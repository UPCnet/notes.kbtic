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
import time
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName

NOTES_USER = "******"
NOTES_PASS = "******"


class NotesSyncKBTIC():

    def __call__(self):
        ###
        ###

        session = requests.session()

        URL = 'https://liszt.upc.es'
        LOGIN_URL = 'https://liszt.upc.es/names.nsf?Login'
        PATH1 = 'BF25AB0F47BA5DD785256499006B15A4'
        PATH = 'C1256E520031DA66/' + PATH1
        BASE_URL = 'https://liszt.upc.es/%s' % PATH
        TRAVERSE_PATH = '/Upcnet/Backoffice/manualexp.nsf/'
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
        limit = 100
        logging.info('Total objects importing: %s to %s', startLimit, limit)
        for index  in range(startLimit, int(limit) + 1):
            if index % 40 == 0:  # Wait every pack of imports...
                time.sleep(10)
                logging.info(' -> 5 seconds pause...')

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
            if 'Incorrect data type for operator or @Function: Text expected<HR>\n<a href="javascript: onClick=history.back()' in html.content:
                logging.info("ERROR in object %s. NOT MIGRATED! URL: %s", index, originNotesObjectUrl)
            else:
                htmlContent = str(html.content)  # .encode('iso-8859-1').decode('utf-8') # PRODUCTION
                # htmlContent = str(html.content).encode('iso-8859-1').decode('utf-8')  # DEVELOP ERROR?
                #htmlContent = str(html.content).decode('iso-8859-1').encode('utf-8')    # CAPRICORNIUS

                logging.info("Migrating object %s, URL: %s", index, originNotesObjectUrl)

                creator = re.search(r'name="From"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]
                Title = re.search(r'(<title>(.*?)</title>)', htmlContent).groups()[1]
                tinyContent = re.search(r'^(.*?)(<script.*/script>)(.*?)(<applet.*/applet)(.*?)(<HEAD.*/HEAD>)(.*?)(.*?)<a\s*href="\/Upcnet\/Backoffice\/manualexp\.nsf\/\(\$All\)\?OpenView">.*$', htmlContent, re.DOTALL | re.MULTILINE).groups()[7]
                object = self.createNotesObject('notesDocument', self.context, Title)

                try:
                    catServei = re.search(r'name="Serveis"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split(', ')
                    for obj in catServei:
                        object.setCategory1(obj)
                except:
                    None
                try:
                    catServeiPPS = re.search(r'name="Productes"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split(', ')
                    for obj in catServeiPPS:
                        object.setCategory2(obj)
                except:
                    None
                # try:
                #     import ipdb; ipdb.set_trace( )
                #     values = re.search(r'name="Categories"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split('\\')
                #     for obj in values:
                #         object.setCategory1(obj)
                # except:
                #     None
                object.setTitle(Title)
                object.setCreators(creator)
                object.setExcludeFromNav(True)
                # Import Images of the object
                imatgeSrc = re.findall(r'<img[^>]+src=\"([^\"]+)\"', htmlContent)
                imatgeSrc = [a for a in imatgeSrc if '/Upcnet' in a]
                numimage = 1
                for obj in imatgeSrc:
                    imatge = session.get(URL + obj, headers=cookie)
                    imageObject = self.createNotesObject('Image', object, 'image' + str(numimage))
                    tinyContent = tinyContent.replace(obj, object.absolute_url() + '/image' + str(numimage))
                    logging.info('Image NSF: %s', object.absolute_url() + '/image' + str(numimage))
                    numimage = numimage + 1
                    imageObject.setImage(imatge.content)

                # Import Files of the object
                attachSrc = re.findall(r'<a[^>]+href=\"([^\"]+)\"', htmlContent)
                attachSrc = [a for a in attachSrc if '$FILE' in a]
                numfile = 1
                for obj in attachSrc:
                    file = session.get(URL + obj, headers=cookie)
                    filename = obj.split('/')[-1].replace('%20', '_')
                    normalizedName = getToolByName(self.context, 'plone_utils').normalizeString(filename)
                    fileObject = self.createNotesObject('File', object, normalizedName)
                    tinyContent = tinyContent.replace(obj, object.absolute_url() + '/' + normalizedName)
                    logging.info('File NSF: %s', object.absolute_url() + '/' + normalizedName)
                    numfile = numfile + 1
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

                # remove section links...
                removeSections = re.findall(r'(<a[^>]+target="_self">.*?</a>)', tinyContent)
                for obj in removeSections:
                    tinyContent = tinyContent.replace(obj, "")

                # Create modified HTML content with new image/file paths
                object.setBody(tinyContent)
                # object.reindexObject()
                transaction.commit()

        logging.info('Done! End of Notes Migration process.')
        return 'OK, imported'

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
