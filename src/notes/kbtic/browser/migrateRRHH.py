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
        PATH1 = '867962c7d68029f085256603006add59'
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
                    'LtpaToken': ''
        }
        # Creating default tree sctructure

        # self.createObject('Folder', self.context, "AGENDA")
        # folder = self.createObject('Folder', self.context, "ASSEGURANÇA")
        # folder.getId()
        # self.createObject('Folder', folder, "2012")
        # self.createObject('Folder', folder, "2011")
        # self.createObject('Folder', self.context, "ASSESSORAMENT")
        # folder = self.createObject('Folder', self.context, "CALENDARI LABORAL")
        # folder.getId()
        # self.createObject('Folder', folder, "2013")
        # self.createObject('Folder', self.context, "CERTIFICATS")
        # folder = self.createObject('Folder', self.context, "COMITE EMPRESA")
        # folder.getId()
        # self.createObject('Folder', folder, "Calendari 2013")
        # folder = self.createObject('Folder', self.context, "COMPTABILITAT")
        # folder.getId()
        # folder2 = self.createObject('Folder', folder, "PRESSUPOST")
        # folder2.getId()
        # folder3 = self.createObject('Folder', folder2, "Pressupost 2011")
        # folder3.getId()
        # self.createObject('Folder', folder3, "Projeccions")
        # folder3 = self.createObject('Folder', folder2, "Pressupost 2012")
        # folder3.getId()
        # self.createObject('Folder', folder3, "Projeccions")
        # self.createObject('Folder', folder3, "Capacitats seguiment")
        # folder3 = self.createObject('Folder', folder2, "Pressupost 2013")
        # folder3.getId()
        # self.createObject('Folder', folder3, "Capacitats 2013")
        # self.createObject('Folder', folder, "IMPOSTOS")
        # folder2 = self.createObject('Folder', folder, "ABC")
        # folder2.getId()
        # self.createObject('Folder', folder2, "2011")
        # self.createObject('Folder', folder, "CANVI ADREÇA FISCAL")
        # self.createObject('Folder', folder, "Auditoria")
        # folder2 = self.createObject('Folder', folder, "Periodificacions")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Capacitats 2011")
        # self.createObject('Folder', folder2, "Capacitats 2012")
        # folder = self.createObject('Folder', self.context, "CONCILIACIÓ")
        # folder.getId()
        # folder2 = self.createObject('Folder', folder, "Mesures Conciliació")
        # folder2.getId()
        # self.createObject('Folder', folder2, "2012")
        # self.createObject('Folder', folder, "Jornada Intensiva Pares")
        # folder = self.createObject('Folder', self.context, "CONTRACTES")
        # folder.getId()
        # self.createObject('Folder', folder, "Models")
        # folder2 = self.createObject('Folder', folder, "PERMIS SENSE SOU")
        # folder2.getId()
        # self.createObject('Folder', folder2, "2012")
        # folder2 = self.createObject('Folder', folder, "CONTRACTES")
        # folder2.getId()
        # folder3 = self.createObject('Folder', folder2, "Contractes 2012")
        # folder3.getId()
        # self.createObject('Folder', folder3, "Estrella Sanchez")
        # self.createObject('Folder', folder3, "Oriol Garcia")
        # self.createObject('Folder', folder3, "Cancel·lació variable")
        # self.createObject('Folder', folder3, "CTTI")
        # self.createObject('Folder', folder2, "Contractes 2011")
        # folder2 = self.createObject('Folder', folder, "VENCIMENTS CONTRACTES/CONVENIS/REDUCCIONS JORNADES")
        # folder2.getId()
        # folder3 = self.createObject('Folder', folder2, "2011")
        # folder3.getId()
        # self.createObject('Folder', folder3, "Venciment contractes")
        # self.createObject('Folder', folder3, "Venciment Convenis")
        # folder3 = self.createObject('Folder', folder2, "2012")
        # folder3.getId()
        # self.createObject('Folder', folder3, "venciments reducció de jornada")
        # self.createObject('Folder', folder3, "Venciment contractes")
        # self.createObject('Folder', folder3, "Venciment Convenis")
        # self.createObject('Folder', folder, "EXCEDÈNCIES")
        # folder2 = self.createObject('Folder', folder, "MATERNITATS")
        # folder2.getId()
        # self.createObject('Folder', folder2, "2011")
        # self.createObject('Folder', folder2, "2012")
        # folder2 = self.createObject('Folder', folder, "Reducció - Ampliació JORNADES")
        # folder2.getId()
        # self.createObject('Folder', folder2, "2011")
        # self.createObject('Folder', folder2, "2012")
        # folder3 = self.createObject('Folder', folder, "Convenis")
        # folder3.getId()
        # self.createObject('Folder', folder3, "2011")
        # self.createObject('Folder', folder3, "2012")
        # self.createObject('Folder', folder3, "2012-2013: RENOVACION CONVENIS")
        # folder2 = self.createObject('Folder', folder, "PATERNITATS")
        # folder2.getId()
        # self.createObject('Folder', folder2, "2011")
        # self.createObject('Folder', folder2, "2012")
        # folder = self.createObject('Folder', self.context, "COSTOS")
        # folder.getId()
        # self.createObject('Folder', folder, "DEG")
        # self.createObject('Folder', folder, "EUETIB")
        # self.createObject('Folder', folder, "Indemnitzacions")
        # folder = self.createObject('Folder', self.context, "DESPESES CORPORATIVES")
        # folder.getId()
        # folder2 = self.createObject('Folder', folder, "Nadales")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Nadales 2011")
        # self.createObject('Folder', folder2, "Nadales 2012")
        # folder2 = self.createObject('Folder', folder, "Teaming")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Dia teaming")
        # self.createObject('Folder', folder, "REGALS")
        # folder = self.createObject('Folder', self.context, "ELECCIONS")
        # folder.getId()
        # self.createObject('Folder', folder, "2011")
        # folder = self.createObject('Folder', self.context, "FORCEM")
        # folder.getId()
        # self.createObject('Folder', folder, "2010")
        # self.createObject('Folder', folder, "2012")
        # self.createObject('Folder', folder, "2011")
        # folder = self.createObject('Folder', self.context, "FORMACIO")
        # folder.getId()
        # self.createObject('Folder', folder, "2010")
        # folder2 = self.createObject('Folder', folder, "2011")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Formació TIC CAT")
        # folder2 = self.createObject('Folder', folder, "2012")
        # folder2.getId()
        # self.createObject('Folder', folder2, "TIC CAT")
        # self.createObject('Folder', folder2, "PRL")
        # self.createObject('Folder', folder, "CERTIFICACIONS")
        # self.createObject('Folder', self.context, "FORUM TI")
        # self.createObject('Folder', self.context, "FOTOGRAFIES")
        # folder = self.createObject('Folder', self.context, "GESTORIA")
        # folder.getId()
        # self.createObject('Folder', folder, "Dades personals")
        # self.createObject('Folder', folder, "Seguretat Social")
        # folder = self.createObject('Folder', self.context, "INDICADORS")
        # folder.getId()
        # folder2 = self.createObject('Folder', folder, "2012")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Absentisme")
        # self.createObject('Folder', folder, "2011")
        # folder = self.createObject('Folder', self.context, "LLISTATS")
        # folder.getId()
        # self.createObject('Folder', folder, "Llistat * centre de treball")
        # folder = self.createObject('Folder', self.context, "NOMINA")
        # folder.getId()
        # folder2 = self.createObject('Folder', folder, "2012")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Quitances")
        # self.createObject('Folder', folder2, "Teaming")
        # self.createObject('Folder', folder2, "Variable")
        # self.createObject('Folder', folder2, "IRPF")
        # folder2 = self.createObject('Folder', folder, "2011")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Quitances")
        # folder = self.createObject('Folder', self.context, "PERFILS I ORGANIGRAMES")
        # folder.getId()
        # self.createObject('Folder', folder, "2012")
        # self.createObject('Folder', folder, "2011")
        # self.createObject('Folder', self.context, "PERMISOS RETRIBUITS")
        # self.createObject('Folder', self.context, "PRESENTACIONS")
        # folder = self.createObject('Folder', self.context, "PRL")
        # folder.getId()
        # self.createObject('Folder', folder, "CONTRACTES")
        # self.createObject('Folder', folder, "FORMACIÓ")
        # folder2 = self.createObject('Folder', folder, "Historics")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Revisions mediques")
        # self.createObject('Folder', folder, "Teletreball")
        # self.createObject('Folder', folder, "Designació treballadors")
        # self.createObject('Folder', folder, "Organigrames")
        # self.createObject('Folder', folder, "Comite Seguretat i Salut")
        # folder = self.createObject('Folder', self.context, "PROJECTES EXTERNS")
        # folder.getId()
        # self.createObject('Folder', folder, "2011")
        # self.createObject('Folder', folder, "2012")
        # folder = self.createObject('Folder', self.context, "RETRIBUCIÓ")
        # folder.getId()
        # folder2 = self.createObject('Folder', folder, "2012")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Març")
        # self.createObject('Folder', folder2, "Juny 2012")
        # self.createObject('Folder', folder2, "Setembre")
        # self.createObject('Folder', folder, "2011")
        # folder = self.createObject('Folder', self.context, "RSC")
        # folder.getId()
        # self.createObject('Folder', folder, "Dades consum i reciclatge 2007-2010")
        # folder = self.createObject('Folder', self.context, "SELECCIO")
        # folder.getId()
        # self.createObject('Folder', folder, "Portals Selecció")
        # folder = self.createObject('Folder', self.context, "SOTSCONTRACTATS")
        # folder.getId()
        # self.createObject('Folder', folder, "Llistat sotscontractats 2011")
        # folder = self.createObject('Folder', self.context, "SUBVENCIONS")
        # folder.getId()
        # folder2 = self.createObject('Folder', folder, "2012")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Investigadors")
        # self.createObject('Folder', folder, "2011")
        # self.createObject('Folder', folder, "GAMCO")
        # folder = self.createObject('Folder', self.context, "TEMES LABORALS")
        # folder.getId()
        # self.createObject('Folder', folder, "TELETREBALL")
        # self.createObject('Folder', folder, "Congelació Salarial")
        # self.createObject('Folder', folder, "VAGA GENERAL")
        # folder2 = self.createObject('Folder', folder, "PLANTILLES")
        # folder2.getId()
        # self.createObject('Folder', folder2, "2012")
        # folder2 = self.createObject('Folder', folder, "SIMULACIONS")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Simulacions Variable")
        # self.createObject('Folder', folder2, "Calendari laboral")
        # folder2 = self.createObject('Folder', folder, "CANVIS EQUIPS")
        # folder2.getId()
        # self.createObject('Folder', folder2, "2011")
        # self.createObject('Folder', folder2, "2012")
        # self.createObject('Folder', folder, "Excedència")
        # self.createObject('Folder', folder, "Estudi jubilacions")
        # folder2 = self.createObject('Folder', folder, "Sancions")
        # folder2.getId()
        # self.createObject('Folder', folder2, "Jose Antonio Rodriguez")
        # folder = self.createObject('Folder', self.context, "VACANCES")
        # folder.getId()
        # self.createObject('Folder', folder, "2011")
        # folder = self.createObject('Folder', self.context, "VARIS")
        # folder.getId()
        # self.createObject('Folder', folder, "Sistemes Informació")
        # self.createObject('Folder', self.context, "Not Categorized")
        # self.createObject('Folder', self.context, "UNSORTED")
        # transaction.commit()


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
        #f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Total objects to import: ' + limit + '\n')
        #logging.info('Total objects to import: %s', limit)
        # View by Date & created by creation
        pack = 'https://liszt.upc.es/Upcnet/RRHH/RecursosHumans.nsf//All Chronological?ReadViewEntries&start=1&count=1000&ExpandView'
        response3 = session.get(pack, headers=cookie)
        UIDs = re.findall(r'unid="(\w+)"', response3.content)
        UIDs.reverse()
        limit = len(UIDs)

        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Total objects to import: ' + str(limit) + '\n')
        logging.info('Total objects to import: %s', limit)
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Total objects importing: ' + str(startLimit) + ' to ' + str(limit) + '\n')
        logging.info('Total objects importing: %s to %s', startLimit, limit)
        objectestotals = [a for a in UIDs[startLimit:(limit + 1)]]
        #startLimit = 0
        #limit = 10
        # Comment!!!
        objectestotals = objectestotals[125:]
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
            lista = []
            try:
                categories = re.search(r'name="Categories"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0].split(', ')
                for obj in categories:
                    id_cat = [result for result in self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', Title=obj) if result.Title == obj][0].id
                    lista = lista + [id_cat]
            except:
                None
            # categories = carpetes a RRHH
            plone_utils = getToolByName(self.context, 'plone_utils')
            try:
                pathcarpeta = re.search(r'name="Categories"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]
            except:
                pathcarpeta = 'Not Categorized'
            idcarpeta = plone_utils.normalizeString(pathcarpeta)
            carpeta = self.context[idcarpeta]

            try:
                pathsubcarpeta = re.search(r'name="ParentSubject"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]
                pathsubcarpeta = 'EXIST'
            except:
                pathsubcarpeta = 'NOT EXIST'

            if pathsubcarpeta == 'EXIST':
                idsubcarpeta = plone_utils.normalizeString(pathsubcarpeta)
                existSubFolder = self.context[idcarpeta].hasObject(idsubcarpeta)

                if not existSubFolder:
                    currentFolder = self.context[idcarpeta]
                    result = [a for a in currentFolder.objectIds()]
                    for obj in result:
                        if self.context[idcarpeta][obj].hasObject(idsubcarpeta):
                            carpeta = self.context[idcarpeta][obj][idsubcarpeta]
                            return
                        else:
                            None
                else:
                    carpeta = self.context[idcarpeta][idsubcarpeta]
            #import ipdb;ipdb.set_trace()
            if self.context[idcarpeta].hasObject(plone_utils.normalizeString(titleObject)):
                titleObject = titleObject + '-1'
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '#' + str(index) + '# ---- RENAMED DOC (folder exists?): ' + str(carpeta) + ' ' + str(titleObject) + ' \n')
            object = self.createNotesObject('documentRRHH', carpeta, titleObject)
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + '$' + str(index) + '$ Notes: ' + str(originNotesObjectUrl) + ' ')
            f.write('Plone: ' + object.absolute_url() + ' \n')

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
                    if extension == 'doc':
                        fileObject.setFormat('application/msword')
                    if extension == 'docx':
                        fileObject.setFormat('application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                    if extension == 'xls':
                         fileObject.setFormat('application/vnd.ms-excel')
                    if extension == 'xlsx':
                        fileObject.setFormat('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    if extension == 'ppt':
                        fileObject.setFormat('application/vnd.ms-powerpoint')
                    if extension == 'pptx':
                        fileObject.setFormat('application/vnd.openxmlformats-officedocument.presentationml.presentation')
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

    def createObject(self, type, folder, title):
        """
        """
        id = self.generateUnusedId(title)
        _createObjectByType(type, folder, id=id, title=title)
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
