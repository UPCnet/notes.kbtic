# -*- coding: utf-8 -*-
#
# From Notes ADS-SPO to Plone
# Remember to customize lines 18,19, 32, 33, 35 and 102
#
# Principal URL: All documents by cateogry:
#    https://liszt.upc.es/upcnet/backoffice/docADS.nsf/BF25AB0F47BA5DD785256499006B15A4
#    Notes://Liszt/C1256E7E00339EE3/BF25AB0F47BA5DD785256499006B15A4
#

import requests
import logging
import re
import transaction
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName

NOTES_USER = "usuari.elena6"
NOTES_PASS = "NotesNotes6"


class NotesSyncADS():

    def __call__(self):
        ###
        ###

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
                            filename='import-KBTIC.log',
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
        'NomUsuari': '%s' % NOTES_USER
        }
        session.cookies.update(extra_cookies)
        response = session.post(LOGIN_URL, params, allow_redirects=True)
        cookie = {'Cookie': 'HabCookie=1; Desti=' + URL + '/' + PATH + '; RetornTancar=1; NomUsuari=' + NOTES_USER + ' LtpaToken=' + session.cookies['LtpaToken']}
        response = requests.get(MAIN_URL, headers=cookie)

        response2 = requests.get(URL + TRAVERSE_PATH + '($All)?OpenView', headers=cookie)
        # Ens quedem ID de la vista
        value = re.search(r'name="ViewUNID"\s+value="(\w+)"', response2.content).groups()[0]

        # url to obtain total entries to import
        toplevelentries = URL + TRAVERSE_PATH + value + '?ReadViewEntries&start=1&count=1'
        startLimit = 1
        xmlLimit = session.get(toplevelentries, headers=cookie)
        limit = re.search(r'toplevelentries="(\w+)"', xmlLimit.content).groups()[0]
        logging.info('Starting Notes Migration process...')
        logging.info('Total objects to import: %s', limit)
        # Uncomment for manual imports...
        startLimit = 1
        limit = 10
        logging.info('Total objects importing: %s to %s', startLimit, limit)
        for index in range(startLimit, int(limit) + 1):
            path_notes = URL + TRAVERSE_PATH + value + '?ReadViewEntries&start=' + str(index) + '&count=1'
            response3 = session.get(path_notes, headers=cookie)
            # No devuelve los mismos resultados, depende de permisos de usuario.
            # La diferencia está en los docs encriptados de contraseñas
            UID = re.search(r'unid="(\w+)"', response3.content).groups()[0]
            # TODO : Check docs with multiple sections (check if values in 3.1 and 3.2 are well imported)
            final_object = URL + TRAVERSE_PATH + value + '/' + UID + '?OpenDocument&ExpandSection=1,2,3,3.1,3.2,4,5,6,7,8,9,10'
            originNotesObjectUrl = URL + TRAVERSE_PATH + value + '/' + UID
            html = session.get(final_object, headers=cookie)
            htmlContent = str(html.content)  # .encode('iso-8859-1').decode('utf-8')
            try:
                titleObject = re.search(r'name="Subject"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('iso-8859-1').replace("&quot;", '"')
            except:
                try:
                    titleObject = re.search(r'(<title>(.*?)</title>)', htmlContent).groups()[1].decode('iso-8859-1').replace("&quot;", '"')
                except:
                    titleObject = 'ERROR: Title not found... Check IT!'
            if 'Incorrect data type for operator or @Function: Text expected<HR>\n<a href="javascript: onClick=history.back()' in html.content:
                logging.info("ERROR in object %s. NOT MIGRATED! URL: %s", index, originNotesObjectUrl)
            else:
                #htmlContent = str(html.content)                                      # PRODUCTION
                htmlContent = str(html.content).decode('iso-8859-1').encode('utf-8')  # GOLLUM

                logging.info("#%s# Migrating: %s", index, originNotesObjectUrl)
                logging.info("#%s# Title: %s", index, titleObject)

                creator = re.search(r'name="From"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]
                Title = titleObject
                tinyContent = re.search(r'^(.*?)(<script.*/script>)(.*?)(<applet.*/applet)(.*?)(<HEAD.*/HEAD>)(.*?)(<a\s*href="\/upcnet\/backoffice\/docADS\.nsf\/\(\$All\)\?OpenView">)(.*?)', htmlContent, re.DOTALL | re.MULTILINE).groups()[6]
                object = self.createNotesObject('notesDocument', self.context, Title)
                logging.info("#%s# URL: %s", index, object.absolute_url())
                try:
                    lista = []
                    catServei = re.search(r'name="Serveis"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split(', ')
                    for obj in catServei:
                        #id_cat = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj)[0].id
                        id_cat = [result for result in self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj) if result.Title == obj][0].id
                        lista = lista + [id_cat]
                        object.setCategory1(lista)
                except:
                    None
                try:
                    lista = []
                    catServeiPPS = re.search(r'name="Productes"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split(', ')
                    for obj in catServeiPPS:
                        #id_cat = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj)[0].id
                        id_cat = [result for result in self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj) if result.Title == obj][0].id
                        lista = lista + [id_cat]
                        object.setCategory2(lista)
                except:
                    None
                try:
                    # sometimes people write with \ separator, we must force check two options...
                    lista = []
                    categories = re.search(r'name="Categories"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split(', ')
                    for obj in categories:
                        #id_cat = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj)[0].id
                        id_cat = [result for result in self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj) if result.Title == obj][0].id
                        lista = lista + [id_cat]
                        object.setCategory3(lista)
                except:
                    None
                try:
                    # sometimes people write with \ separator, we must force check two options...
                    lista = []
                    categories = re.search(r'name="Categories"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split('\\')
                    for obj in categories:
                        #id_cat = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj)[0].id
                        id_cat = [result for result in self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj) if result.Title == obj][0].id

                        lista = lista + [id_cat]
                        object.setCategory3(lista)

                except:
                    None
                object.setTitle(Title)
                object.setCreators(creator)
                object.setExcludeFromNav(True)

                # Import Images of the object
                imatgeSrc = re.findall(r'<img[^>]+src=\"([^\"]+)\"', htmlContent)
                imatgeSrc = [a for a in imatgeSrc if '/upcnet' in a]
                numimage = 1
                for obj in imatgeSrc:
                    imatge = session.get(URL + obj, headers=cookie)
                    imageObject = self.createNotesObject('Image', object, 'image' + str(numimage))
                    tinyContent = tinyContent.replace(obj, object.absolute_url() + '/image' + str(numimage))
                    logging.info('#%s# Creating image: %s', index, object.absolute_url() + '/image' + str(numimage))
                    numimage = numimage + 1
                    imageObject.setImage(imatge.content)

                # Import Files of the object
                attachSrc = re.findall(r'<a[^>]+href=\"([^\"]+)\"', htmlContent)
                attachSrc = [a for a in attachSrc if '$FILE' in a]
                for obj in attachSrc:
                    try:
                        file = session.get(URL + obj, headers=cookie)
                        filename = obj.split('/')[-1].replace('%20', '_').replace('_', '')
                        normalizedName = getToolByName(self.context, 'plone_utils').normalizeString(filename)
                        # fake the same filename in folder object...
                        contents = object.contentIds()
                        normalizedName = self.calculaNom(contents, normalizedName)
                        fileObject = self.createNotesObject('File', object, normalizedName)
                        tinyContent = tinyContent.replace(obj, object.absolute_url() + '/' + normalizedName)
                        logging.info('#%s# Creating file: %s', index, object.absolute_url() + '/' + normalizedName)
                        fileObject.setFile(file.content)
                        # OpenOffice files internally are saved as ZIP files, we must force metadata...
                        extension = obj.split('.')[-1:][0]
                        if extension == 'odt':
                            fileObject.setFormat('application/vnd.oasis.opendocument.text')
                        if extension == 'ods':
                            fileObject.setFormat('application/vnd.oasis.opendocument.spreadsheet')
                        if extension == 'odp':
                            fileObject.setFormat('application/vnd.oasis.opendocument.presentation')
                        if extension == 'odg':
                            fileObject.setFormat('application/vnd.oasis.opendocument.graphics')
                    except:
                        logging.info('#%s# ERROR IMPORTING OBJECT! CHECK IT!', index)
                        pass
                # remove section links...
                removeSections = re.findall(r'(<a[^>]+target="_self">.*?</a>)', tinyContent)
                for obj in removeSections:
                    tinyContent = tinyContent.replace(obj, "")
                # Create modified HTML content with new image/file paths
                object.setBody(tinyContent)
                object.reindexObject()
                transaction.commit()
                # Fix creation Date
                try:
                    Date = re.search(r'name="Date"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('iso-8859-1').replace("&quot;", '"')
                    if Date == 'Yesterday':
                        import datetime
                        today = datetime.date.today()
                        dateCreatedInNotes = str(today.year) + '-' + str(today.month) + '-' + str(today.day - 1)
                        object.setCreationDate(dateCreatedInNotes)
                    else:
                        dateCreatedInNotes = Date.split('/')[2] + '/' + Date.split('/')[0] + '/' + Date.split('/')[1]
                        object.setCreationDate(dateCreatedInNotes)
                except:
                    pass
                try:
                    Date = re.search(r'name="DateComposed"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('iso-8859-1').replace("&quot;", '"')
                    dateCreatedInNotes = '2012/' + Date.split('/')[1] + '/' + Date.split('/')[0]
                    object.setCreationDate(dateCreatedInNotes)
                except:
                    pass
                transaction.commit()
                logging.info('#%s# Object migrated', index)

        logging.info('Done! End of Notes Migration process.')
        return 'OK, imported'

    def calculaNom(self, ids, nom_normalitzat, i=0):
        """
        """
        if i != 0:
            nom = nom_normalitzat + str(i)
        else:
            nom = nom_normalitzat
        if nom not in ids:
            return nom
        else:
            return self.calculaNom(ids, nom_normalitzat, i + 1)

    def createNotesObject(self, type, folder, title):
        """
        """
        id = self.generateUnusedId(title)
        _createObjectByType(type, folder, id)
        obj = folder[id]

        return obj

    def generateUnusedId(self, title):
        """
        """
        plone_utils = getToolByName(self.context, 'plone_utils')
        id = plone_utils.normalizeString(title)
        if id in self.context.contentIds():
            number = 2
            while '%s-%i' % (id, number) in self.context.contentIds():
                number += 1
            id = '%s-%i' % (id, number)
        return id


### EOF ###
