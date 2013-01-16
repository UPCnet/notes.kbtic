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

### EOF ###
