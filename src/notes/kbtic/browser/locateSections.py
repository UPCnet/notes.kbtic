# -*- coding: utf-8 -*-
#
# From Notes KBTIC to Plone
# Remember to customize lines 18,19, 32, 33, 35 and 102
#
# Principal URL: All documents by cateogry:
#    https://liszt.upc.es/upcnet/backoffice/manualexp.nsf/BF25AB0F47BA5DD785256499006B15A4
#    Notes://Liszt/C1256E520031DA66/BF25AB0F47BA5DD785256499006B15A4
#

import requests
import logging
import re
import transaction
from pyquery import PyQuery as pq

NOTES_USER = ""
NOTES_PASS = ""


class locateSectionsKBTIC():

    def __call__(self):
        ###
        ###
        from datetime import datetime
        session = requests.session()

        URL = 'https://liszt.upc.es'
        LOGIN_URL = 'https://liszt.upc.es/names.nsf?Login'
        PATH1 = 'C1256E520031DA66/BF25AB0F47BA5DD785256499006B15A4'
        PATH = 'C1256E520031DA66/' + PATH1
        BASE_URL = 'https://liszt.upc.es/%s' % PATH
        TRAVERSE_PATH = '/Upcnet/Backoffice/manualexp.nsf/'
        MAIN_URL = 'https://liszt.upc.es' + TRAVERSE_PATH + PATH1 + '?ReadViewEntries&PreFormat&Start=1&Navigate=16&Count=1000000064&SkipNavigate=32783&EndView=1'

        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filename='locateSections-KBTIC.log',
                            level=logging.DEBUG)

        params = {
                    'RedirectTo': '/' + PATH,
                    'Servidor': 'schubert.upc.es/helpaute.nsf/',
                    'Username': '%s' % NOTES_USER,
                    'Password': '%s' % NOTES_PASS,
                 }

        extra_cookies = {
            'HabCookie': '1',
            'Desti': BASE_URL,
            'NomUsuari': '%s' % NOTES_USER,
            'LtpaToken': 'AAECAzUwRjNDRkJENTBGM0U0RDVDTj1Sb2JlcnRvIERpYXovTz1VcGNuZXTdGFrqj9xWkBx1YuZSGqw4W1Hlng=='
        }

        session.cookies.update(extra_cookies)
        response = session.post(LOGIN_URL, params, allow_redirects=True)
        cookie = {'Cookie': 'HabCookie=1; Desti=' + URL + '/' + PATH + '; RetornTancar=1; NomUsuari=' + NOTES_USER + ' LtpaToken=' + session.cookies['LtpaToken']}
        response = requests.get(MAIN_URL, headers=cookie)
        response2 = requests.get(URL + TRAVERSE_PATH + '($All)?OpenView', headers=cookie)
        #data = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        #f = open('locateSections-' + data + '.log', 'a')  # PROD
        f = open('locateSectionsKBTIC.log', 'a')  # GOLLUM
        value = re.search(r'name="ViewUNID"\s+value="(\w+)"', response2.content).groups()[0]
        toplevelentries = URL + TRAVERSE_PATH + value + '?ReadViewEntries&start=1&count=1'
        startLimit = 1
        xmlLimit = session.get(toplevelentries, headers=cookie)
        limit = re.search(r'toplevelentries="(\w+)"', xmlLimit.content).groups()[0]
        f.write('-----------------------------------------------------------------------------' + '\n')
        logging.info('------------------------------------------------------')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Logging sections from KBTIC docs... (Real limit: ' + limit + ')' + '\n')
        logging.info('Logging sections from KBTIC docs... (Real limit: %s)', limit)
        # Uncomment for manual imports...
        startLimit = 1340
        limit = 4000
        index = 1340
        uid_list = []
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Objects to check: ' + str(startLimit) + ' to ' + str(limit) + '\n')
        logging.info('Objects to check: %s to %s', startLimit, limit)
        for index in range(startLimit, int(limit) + 1):
            path_notes = URL + TRAVERSE_PATH + value + '?ReadViewEntries&start=' + str(index) + '&count=1'
            #logging.info('#%s# PathNotes: %s', index, path_notes)
            response3 = session.get(path_notes, headers=cookie)
            UID = re.search(r'unid="(\w+)"', response3.content).groups()[0]
            # removes repeated...
            if UID not in uid_list:
                uid_list = uid_list + [UID]
                final_object = URL + TRAVERSE_PATH + value + '/' + UID + '?OpenDocument&ExpandSection=1,2,3,3.1,3.2,4,5,6,7,8,9,10'
                originNotesObjectUrl = URL + TRAVERSE_PATH + value + '/' + UID
                #logging.info('#%s# NotesURL: %s', index, originNotesObjectUrl)
                html = session.get(final_object, headers=cookie)
                htmlContent = str(html.content)
                sections = re.findall(r'^<a name="(.*?)"></a>', htmlContent, re.DOTALL | re.MULTILINE)
                try:
                    titleObject = re.search(r'name="Subject"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('utf-8').replace("&quot;", '"').replace("&lt;", '<').replace("&gt;", '>')
                except:
                    if 'Incorrect data type for operator or @Function: ' in html.content:
                        titleObject = 'ERROR in locateKBTIC'
                    else:
                        titleObject = re.search(r'(<title>(.*?)</title>)', htmlContent).groups()[1].decode('iso-8859-1').replace("&quot;", '"').replace("&lt;", '<').replace("&gt;", '>')
                if 'Incorrect data type for operator or @Function: ' in html.content:
                    logging.info("ERROR in object %s. NOT MIGRATED! URL: %s", index, originNotesObjectUrl)
                else:
                    from datetime import datetime
                    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# Title: ' + str(titleObject) + '\n')
                    #logging.info('#%s# %s', index, titleObject)
                    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '$ Notes: ' + str(originNotesObjectUrl) + '\n')
                    #logging.info('#%s# %s', index, originNotesObjectUrl)
                    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# Sections: ' + str(sections) + '\n')
                    logging.info('#%s# %s', index, sections)
                    index = index + 1
            else:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# UID exists: ' + UID + ' \n')
                logging.info("#%s# UID exists: %s ", index, UID)
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Done!' + '\n')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '--------------------------------------------------' + '\n')
        f.close()
        logging.info('Done!')
        logging.info('------------------------------------------------------')
        return 'OK! Done'


class locateSectionsADS():

    def __call__(self):
        ###
        ###
        from datetime import datetime
        session = requests.session()

        URL = 'https://liszt.upc.es'
        LOGIN_URL = 'https://liszt.upc.es/names.nsf?Login'
        PATH1 = 'BF25AB0F47BA5DD785256499006B15A4'
        PATH = 'C1256E7E00339EE3/' + PATH1
        BASE_URL = 'https://liszt.upc.es/%s' % PATH
        TRAVERSE_PATH = '/upcnet/backoffice/docADS.nsf/'
        MAIN_URL = 'https://liszt.upc.es' + TRAVERSE_PATH + PATH1 + '?ReadViewEntries&PreFormat&Start=1&Navigate=16&Count=1000000064&SkipNavigate=32783&EndView=1'

        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filename='locateSections-ADS.log',
                            level=logging.DEBUG)

        params = {
                    'RedirectTo': '/' + PATH,
                    'Servidor': 'schubert.upc.es/helpaute.nsf/',
                    'Username': '%s' % NOTES_USER,
                    'Password': '%s' % NOTES_PASS,
                 }

        extra_cookies = {
            'HabCookie': '1',
            'Desti': BASE_URL,
            'NomUsuari': '%s' % NOTES_USER,
            'LtpaToken': 'AAECAzUwRjUzNDNGNTBGNTQ5NTdDTj1Sb2JlcnRvIERpYXovTz1VcGNuZXRLgKiMzlJXHrX8oRx27nO2o6a7eA=='
        }

        session.cookies.update(extra_cookies)
        response = session.post(LOGIN_URL, params, allow_redirects=True)
        cookie = {'Cookie': 'HabCookie=1; Desti=' + URL + '/' + PATH + '; RetornTancar=1; NomUsuari=' + NOTES_USER + ' LtpaToken=' + session.cookies['LtpaToken']}
        response = requests.get(MAIN_URL, headers=cookie)
        response2 = requests.get(URL + TRAVERSE_PATH + '($All)?OpenView', headers=cookie)
        data = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        #f = open('locateSections-' + data + '.log', 'a')  # PROD
        f = open('locateSectionsADS.log', 'a')  # GOLLUM
        value = re.search(r'name="ViewUNID"\s+value="(\w+)"', response2.content).groups()[0]
        toplevelentries = URL + TRAVERSE_PATH + value + '?ReadViewEntries&start=1&count=1'
        startLimit = 1
        xmlLimit = session.get(toplevelentries, headers=cookie)
        limit = re.search(r'toplevelentries="(\w+)"', xmlLimit.content).groups()[0]
        f.write('-----------------------------------------------------------------------------' + '\n')
        logging.info('------------------------------------------------------')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Logging sections from ADS docs... (Real limit: ' + limit + ')' + '\n')
        logging.info('Logging sections from ADS docs... (Real limit: %s)', limit)
        # Uncomment for manual imports...
        startLimit = 1
        limit = 4000
        index = 1
        uid_list = []
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Objects to check: ' + str(startLimit) + ' to ' + str(limit) + '\n')
        logging.info('Objects to check: %s to %s', startLimit, limit)
        for index in range(startLimit, int(limit) + 1):
            path_notes = URL + TRAVERSE_PATH + value + '?ReadViewEntries&start=' + str(index) + '&count=1'
            #logging.info('#%s# PathNotes: %s', index, path_notes)
            response3 = session.get(path_notes, headers=cookie)
            UID = re.search(r'unid="(\w+)"', response3.content).groups()[0]
            # removes repeated...
            if UID not in uid_list:
                uid_list = uid_list + [UID]
                final_object = URL + TRAVERSE_PATH + value + '/' + UID + '?OpenDocument&ExpandSection=1,2,3,3.1,3.2,4,5,6,7,8,9,10'
                originNotesObjectUrl = URL + TRAVERSE_PATH + value + '/' + UID
                #logging.info('#%s# NotesURL: %s', index, originNotesObjectUrl)
                html = session.get(final_object, headers=cookie)
                htmlContent = str(html.content)
                sections = re.findall(r'^<a name="(.*?)"></a>', htmlContent, re.DOTALL | re.MULTILINE)
                try:
                    titleObject = re.search(r'name="Subject"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('utf-8').replace("&quot;", '"').replace("&lt;", '<').replace("&gt;", '>')
                except:
                    if 'Incorrect data type for operator or @Function: ' in html.content:
                        titleObject = 'ERROR in locateADS'
                    else:
                        titleObject = re.search(r'(<title>(.*?)</title>)', htmlContent).groups()[1].decode('iso-8859-1').replace("&quot;", '"').replace("&lt;", '<').replace("&gt;", '>')
                if 'Incorrect data type for operator or @Function: ' in html.content:
                    logging.info("ERROR in object %s. NOT MIGRATED! URL: %s", index, originNotesObjectUrl)
                else:
                    from datetime import datetime
                    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# Title: ' + str(titleObject) + '\n')
                    #logging.info('#%s# %s', index, titleObject)
                    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '$ Notes: ' + str(originNotesObjectUrl) + '\n')
                    #logging.info('#%s# %s', index, originNotesObjectUrl)
                    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# Sections: ' + str(sections) + '\n')
                    logging.info('#%s# %s', index, sections)
                    index = index + 1
            else:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# UID exists: ' + UID + ' \n')
                logging.info("#%s# UID exists: %s ", index, UID)
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Done!' + '\n')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '--------------------------------------------------' + '\n')
        f.close()
        logging.info('Done!')
        logging.info('------------------------------------------------------')
        return 'OK! Done'


class setCatalanLang():

    def __call__(self):
        ###
        ###
        results = []
        search_path = '/kbtic/portal_vocabularies/categoryADS_keywords'
        results = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', path = search_path,  Language= 'en')
        for obj in results:
            objecte = obj.getObject()
            objecte.setLanguage('ca')

class ModifyCategory3():

    def __call__(self):
        ### cat3 must contain 'categoria-xxx' and catADS must contain 'ads-xxx'
        ### there was an error and we must to swap the incorrect values
        from datetime import datetime

        filesystem = open('modifyCat3.log', 'a')
        results = []
        search_path = '/kbtic/ads-spo'
        results = self.context.portal_catalog.searchResults(portal_type='notesDocument', path=search_path, )
        logging.info("# REPLACE CATEGORIES START" + '\n')
        for obj in results:
            objecte = obj.getObject()
            cat3 = objecte.getCategory3()
            catADS = objecte.getCategoryADS()
            logging.info("# OLD CAT3: %s URL: %s", cat3, objecte.absolute_url())
            logging.info("# OLD CATADS: %s URL: %s", catADS, objecte.absolute_url())
            if len(cat3) == 0:
                # Categoria buida, no fer res
                logging.info("# CAT3 EMPTY, NOTHING TO DO... URL: %s", objecte.absolute_url())
            else:
                ads_in_cat3 = tuple([a for a in objecte.getCategory3() if 'ads-' in a])
                categoria_in_cat3 = tuple([a for a in objecte.getCategory3() if 'categoria-' in a])
                ads_in_catADS = tuple([a for a in objecte.getCategoryADS() if 'ads-' in a])
                categoria_in_catADS = tuple([a for a in objecte.getCategoryADS() if 'categoria-' in a])

                totCAT3 = categoria_in_cat3 + categoria_in_catADS
                totADS = ads_in_cat3 + ads_in_catADS

                objecte.setCategory3(totCAT3)
                objecte.setCategoryADS(totADS)

                objecte.reindexObject()
                transaction.commit()
                newCat3 = objecte.getCategory3()
                newCatADS = objecte.getCategoryADS()
                logging.info("# CHANGE -> NEW CAT3: %s URL: %s", newCat3, objecte.absolute_url())
                logging.info("# CHANGE -> NEW CATADS: %s URL: %s", newCatADS, objecte.absolute_url())
                filesystem.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '' + objecte.absolute_url() + '\n')
        logging.info("# REPLACE CATEGORIES END" + '\n')
        logging.info("# --------------------------" + '\n')


class ModifyContentContainingColomers():
    """ After creating content, saving html creates automatic relative links to current path of script
        (in this case colomers:11001) :( We need to change colomers to real path...  """
    def __call__(self):
        """ locate content colomers and replace it ... """
        from datetime import datetime
        filesystem = open('modifyContentColomers.log', 'a')
        results = []
        search_path = '/kbtic/ads-spo'
        results = self.context.portal_catalog.searchResults(portal_type='notesDocument', path=search_path, )
        logging.info("# REPLACE CONTENT COLOMERS START" + '\n')
        lista = " Objectes Modificats \n---------------------\n\n"
        for obj in results:
            realURL = 'https://kbtic.upcnet.es/' + '/'.join(obj.getURL().split('/')[4:])
            HTML_PAGE_WITH_LINK = requests.get(realURL, auth=('admin', '**********')).content
            d = pq(HTML_PAGE_WITH_LINK)
            content = d("#parent-fieldname-body").html()
            if 'colomers:11001' in content:
                replacedContent = content.replace("http://colomers:11001/", 'https://kbtic.upcnet.es/')
                objecte = obj.getObject()
                objecte.setBody(replacedContent)
                objecte.indexObject()
                transaction.commit()
                filesystem.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Replaced Content Colomers: ' + objecte.absolute_url() + '\n')
                filesystem.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Content with literal: colomers -> ' + obj.getURL() + '\n')
                logging.info("Object to replace: %s ", obj.getURL())
                lista = lista + obj.getURL() + '\n'
            else:
                filesystem.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'NOT Replaced content: ' + obj.getURL() + '\n')
                logging.info("NOT REPLACED: %s ", obj.getURL())
                #lista = lista + obj.getURL() + '\n'
        filesystem.write('-----------------------------------------------------------------------------' + '\n')
        filesystem.write('                             END: CONTENT COLOMERS' + '\n')
        filesystem.write('-----------------------------------------------------------------------------' + '\n')
        filesystem.close()
        logging.info("END CONTENT COLOMERS process!")

        return lista


### EOF ###
