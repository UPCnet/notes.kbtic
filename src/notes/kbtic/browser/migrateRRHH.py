# -*- coding: utf-8 -*-
#
# From Notes KBTIC to Plone
# Remember to customize lines 18,19, 32, 33, 35 and 102
#
# Principal URL: All documents by cateogry:
#    https://liszt.upc.es/upcnet/backoffice/manualexp.nsf/BF25AB0F47BA5DD785256499006B15A4
#    Notes://Liszt/C1256E520031DA66/BF25AB0F47BA5DD785256499006B15A4
#    https://liszt.upc.es/Upcnet/RRHH/RecursosHumans.nsf

import requests
import logging
import re
import transaction
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName

NOTES_USER = ""
NOTES_PASS = ""


class NotesSyncRRHH():

    def __call__(self):
        ### LtpaToken)
        ###

        session = requests.session()

        URL = 'https://liszt.upc.es'
        LOGIN_URL = 'https://liszt.upc.es/names.nsf?Login'
        PATH1 = '7766194d3ac2abb7852568d900410f40'
        PATH = 'C12578160036BF11/' + PATH1
        BASE_URL = 'https://liszt.upc.es/%s' % PATH
        TRAVERSE_PATH = '/Upcnet/RRHH/RecursosHumans.nsf/'
        MAIN_URL = 'https://liszt.upc.es' + TRAVERSE_PATH

        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filename='import-RRHH.log',
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
        }
        #'LtpaToken': 'AAECAzUwOUE4OEU2NTA5QTlERkVDTj1Sb2JlcnRvIERpYXovTz1VcGNuZXSGtJW/Vw0dtSoxUPqm907yNONwwg=='        
        session.cookies.update(extra_cookies)
        response = session.post(LOGIN_URL, params, allow_redirects=True)
        cookie = {'Cookie': 'HabCookie=1; Desti=' + URL + '/' + PATH + '; RetornTancar=1; NomUsuari=' + NOTES_USER + ' LtpaToken=' + session.cookies['LtpaToken']}
        response = requests.get(MAIN_URL + PATH1, headers=cookie)
        from datetime import datetime
        data = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        #f = open('migrateRRHH-' + data + '.log', 'a')  # PROD
        f = open('migrateRRHH.log', 'a')  # GOLLUM
        startLimit = 0
        xmlLimit = session.get(BASE_URL + '?ReadViewEntries&ExpandView', headers=cookie)
        limit = re.search(r'children="(\w+)"', xmlLimit.content).groups()[0]
        f.write('-----------------------------------------------------------------------------' + '\n')
        logging.info('------------------------------------------------------')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Starting Notes RRHH Migration process...' + '\n')
        logging.info('Starting Notes RRHH Migration process...')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Total objects to import: ' + limit + '\n')
        logging.info('Total objects to import: %s', limit)
        pack = BASE_URL + '?ReadViewEntries&start=1&count=1000&ExpandView'
        response3 = session.get(pack, headers=cookie)
        UIDs = re.findall(r'unid="(\w+)"', response3.content)
        limit = len(UIDs)

        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Total objects to import: ' + str(limit) + '\n')
        logging.info('Total objects to import: %s', limit)
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Total objects importing: ' + str(startLimit) + ' to ' + str(limit) + '\n')
        logging.info('Total objects importing: %s to %s', startLimit, limit)
        objectestotals = [a for a in UIDs[startLimit:(limit + 1)]]
        #startLimit = 0
        #limit = 10
        # Comment!!!
        objectestotals = objectestotals[603:]
        index = 1
        for obj in objectestotals:
            final_object = BASE_URL + '/' + obj + '/' + '?OpenDocument&ExpandSection=1,2,3,3.1,3.2,4,5,6,7,8,9,10'

            originNotesObjectUrl = BASE_URL + '/' + obj
            html = session.get(final_object, headers=cookie)
            htmlContent = str(html.content)
            try:
                titleObject = re.search(r'name="Subject"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('utf-8').replace("&quot;", '"')
            except:
                titleObject = re.search(r'(<title>(.*?)</title>)', htmlContent).groups()[1].decode('utf-8').replace("&quot;", '"')
            if titleObject.lower() == "":
                titleObject = titleObject + ' (RE: ' + re.search(r'name="ParentSubject"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('utf-8').replace("&quot;", '"') + ')'
            if titleObject.lower() == "view":
                titleObject = titleObject + ' (RE: ' + re.search(r'name="ParentSubject"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('utf-8').replace("&quot;", '"') + ')'
            if titleObject.lower() == "keys":
                titleObject = titleObject + ' (RE: ' + re.search(r'name="ParentSubject"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('utf-8').replace("&quot;", '"') + ')'
            htmlContent = str(html.content)

            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# Title: ' + str(titleObject) + '\n')
            logging.info('#%s# %s', index, titleObject)

            creator = re.search(r'name="From"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]
            tinyContent = re.search(r'^(.*?)(<script.*/script>)(.*?)(<applet.*/applet>)(.*?)(<a\s*href=\/Upcnet\/RRHH\/RecursosHumans.nsf\/(.[$]All).[?]OpenView>).*$', htmlContent, re.DOTALL | re.MULTILINE).groups()[4]
            try:
                deleteLink = re.search(r'(.*?)(<a\s*href=.*Icon"></a>)(.*?)', tinyContent).groups()[1]
                tinyContent = tinyContent.replace(deleteLink, '')
            except:
                pass

            object = self.createNotesObject('documentRRHH', self.context, titleObject)
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '$' + str(index) + '$ Notes: ' + str(originNotesObjectUrl) + ' ')
            f.write('Plone: ' + object.absolute_url() + ' \n')
            lista = []
            try:
                categories = re.search(r'name="Categories"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split(', ')
                for obj in categories:
                    id_cat = [result for result in self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj) if result.Title == obj][0].id
                    lista = lista + [id_cat]
            except:
                None
            object.setCategoryRRHH(lista)
            object.setTitle(titleObject)
            object.setCreators(creator)
            object.setExcludeFromNav(True)

            # Import Images of the object
            imatgeSrc = re.findall(r'<img[^>]+src=\"([^\"]+)\"', htmlContent)
            imatgeSrc = [a for a in imatgeSrc if '/Upcnet' in a]
            numimage = 1
            for obj in imatgeSrc:
                imatge = session.get(URL + obj, headers=cookie)
                imageObject = self.createNotesObject('Image', object, 'image' + str(numimage))
                replacedName = (object.absolute_url() + '/image' + str(numimage)).replace('mohinder:8080', 'gw4.beta.upcnet.es')
                tinyContent = tinyContent.replace(obj, replacedName)
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# Creating image: ' + replacedName + '\n')
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
                    replacedName = (object.absolute_url() + '/' + normalizedName).replace('mohinder:8080', 'gw4.beta.upcnet.es')
                    tinyContent = tinyContent.replace(obj, replacedName)
                    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# Creating file: ' + replacedName + '\n')
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
                    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# ERROR IMPORTING OBJECT! CHECK IT!' + '\n')
                    pass

            # remove section links...
            removeSections = re.findall(r'(<a[^>]+target="_self">.*?</a>)', tinyContent)
            for obj in removeSections:
                tinyContent = tinyContent.replace(obj, "")
            # Create modified HTML content with new image/file paths
            object.setBody(tinyContent)

            # Fix creation Date
            try:
                Date = re.search(r'name="Date"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('utf-8').replace("&quot;", '"')
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
                Date = re.search(r'name="DateComposed"\s+type="hidden"\s+value="(.*?)"', htmlContent).groups()[0].decode('utf-8').replace("&quot;", '"')
                dateCreatedInNotes = '2012/' + Date.split('/')[0] + '/' + Date.split('/')[1]
                object.setCreationDate(dateCreatedInNotes)
            except:
                pass

            # Guardar links a BBDD Notes
            links = re.findall(r'<a[^>]+href=\"([^\"]+)\"', tinyContent)
            linksNotes = [a for a in links if '?OpenDocument' in a and not 'Section' in a]
            for obj in linksNotes:
                try:
                    f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# #Link: ' + str(URL) + str(obj) + ' ' + object.absolute_url() + '\n')
                except:
                    pass

            transaction.commit()
            object.reindexObject()
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# Object migrated' + '\n')
            index = index + 1

        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Done! End of Notes Migration process.' + '\n')
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '--------------------------------------------------' + '\n')
        f.close()
        logging.info('Done! End of Notes Migration process.')
        logging.info('------------------------------------------------------')
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
