# -*- coding: utf-8 -*-
# From Notes KBTIC to Plone
#
# Principal URL: All documents by cateogry:
#    https://liszt.upc.es/upcnet/backoffice/manualexp.nsf/BF25AB0F47BA5DD785256499006B15A4
#
import requests
import logging
import re
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName

NOTES_USER = "******"
NOTES_PASS = "******"


class NotesSync():

    def __call__(self):
        ###
        ###

        session = requests.session()
        PATH = 'C1256E520031DA66/BF25AB0F47BA5DD785256499006B15A4'
        URL = 'https://liszt.upc.es'
        LOGIN_URL = 'https://liszt.upc.es/names.nsf?Login'
        BASE_URL = 'https://liszt.upc.es/%s' % PATH
        MAIN_URL = 'https://liszt.upc.es/Upcnet/Backoffice/manualexp.nsf/BF25AB0F47BA5DD785256499006B15A4?ReadViewEntries&PreFormat&Start=1&Navigate=16&Count=1000000064&SkipNavigate=32783&EndView=1'

        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filename='example.log',
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

        cookie = {'Cookie': 'HabCookie=1; Desti=https://liszt.upc.es/C1256E520031DA66/BF25AB0F47BA5DD785256499006B15A4; RetornTancar=1; NomUsuari=usuari.elena6; LtpaToken=' + session.cookies['LtpaToken']}
        response = requests.get(MAIN_URL, headers=cookie)

        response2 = requests.get(URL + '/Upcnet/Backoffice/manualexp.nsf/($All)?OpenView', headers=cookie)
        # Ens quedem ID de la vista
        value = re.search(r'name="ViewUNID"\s+value="(\w+)"', response2.content).groups()[0]

        # XML All documents (limited to 1040):
        # https://liszt.upc.es/Upcnet/Backoffice/manualexp.nsf/626E6035EADBB4CD85256499006B15A6?ReadViewEntries&start=1&count=1000
        #/Upcnet/Backoffice/manualexp.nsf/626E6035EADBB4CD85256499006B15A6?ReadDesign&start=1&count=100000

        # url to obtain total entries to import
        toplevelentries = URL + '/Upcnet/Backoffice/manualexp.nsf/' + value + '?ReadViewEntries&start=1&count=1'
        xmlLimit = session.get(toplevelentries, headers=cookie)
        limit = re.search(r'toplevelentries="(\w+)"', xmlLimit.content).groups()[0]
        logging.info('Starting Notes Migration process...')
        logging.info('Total objects to import: %s', limit)
        limit = 20
        for index  in range(1, int(limit)):

            path_notes = URL + '/Upcnet/Backoffice/manualexp.nsf/' + value + '?ReadViewEntries&start=' + str(index) + '&count=1'
            response3 = session.get(path_notes, headers=cookie)

            # No devuelve los mismos resultados, depende de permisos de usuario.
            # La diferencia está en los docs encriptados de contraseñas

            UID = re.search(r'unid="(\w+)"', response3.content).groups()[0]
            # TODO : Check docs with multiple sections (check if values in 3.1 and 3.2 are well imported)
            final_object = URL + '/Upcnet/Backoffice/manualexp.nsf/' + value + '/' + UID + '?OpenDocument&ExpandSection=1,2,3,3.1,3.2,4,5,6,7,8,9,10'
            originNotesObjectUrl = URL + '/Upcnet/Backoffice/manualexp.nsf/' + value + '/' + UID
            html = session.get(final_object, headers=cookie)
            htmlContent = str(html.content).decode('ISO-8859-1')
            logging.info("Migrating object %s , Notes URL: %s", index, originNotesObjectUrl)
            # Check the kind of document
            try:
                tipusDocument = re.search(r'name="TipusDoc"\s+type="hidden"\s+value="(\w+)"', htmlContent).groups()[0]
            except:
                tipusDocument = "Not_RIN"

            if tipusDocument == "RIN":
                ## RIN document has a table in the footer of the html

                #dateCreated = re.search(r'name="Date"\s+type="hidden"\s+value="(\w+.*)"', htmlContent).groups()[0]
                #timeCreated = "Time of Creation not present in RIN docs"
                #import ipdb; ipdb.set_trace( )
                creator = re.search(r'name="From"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]
                Title = re.search(r'(<title>(.*?)</title>)', htmlContent).groups()[1]
                # ERROR en rins a veces no tiene key subject -> Title = re.search(r'name="Subject"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]

                # 1st version = re.sub(r'^(.*?)(<script.*/script>)(.*?)(<applet.*/applet)(.*?)(<HEAD.*/HEAD>)(.*?)(<table.*?/table>)(.*?)<a\s*href="\/Upcnet\/Backoffice\/manualexp\.nsf\/\(\$All\)\?OpenView">.*$', r'\9', htmlContent, re.DOTALL | re.MULTILINE)
                tinyContent = re.sub(r'^(.*?)(<script.*/script>)(.*?)(<applet.*/applet)(.*?)(<HEAD.*/HEAD>)(.*?)(<hr.*?<table.*?/table>.*?)(.*?)<a\s*href="\/Upcnet\/Backoffice\/manualexp\.nsf\/\(\$All\)\?OpenView">.*$', r'\9', htmlContent, re.DOTALL | re.MULTILINE)

                object = self.createNotesObject('notesDocument', self.context, Title)
                object.setTitle(Title)
                object.setBody(tinyContent)
                object.setCreators(creator)
                object.setExcludeFromNav(True)
                try:
                    catServei = re.search(r'name="Serveis"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]
                    object.setCategory1(catServei)
                except:
                    None
                try:
                    catServeiPPS = re.search(r'name="Productes"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]
                    object.setCategory2(catServeiPPS)
                except:
                    None

                object.reindexObject()

            else:
                ## Normal document doesn't has table in footer, but has 2 tables inside another table

                # 1st version = re.sub(r'^(.*?)(<script.*/script>)(.*?)(<applet.*/applet)(.*?)(<HEAD.*/HEAD>)(.*?)<a\s*href="\/Upcnet\/Backoffice\/manualexp\.nsf\/\(\$All\)\?OpenView">.*$', r'\7', html.content, re.DOTALL | re.MULTILINE)
                #dateCreated = re.search(r'name="Date"\s+type="hidden"\s+value="(\w+.*)"', htmlContent).groups()[0]
                #timeCreated = re.search(r'name="TimeCreated"\s+type="hidden"\s+value="(\w+.*)"', htmlContent).groups()[0]
                creator = re.search(r'name="From"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]
                Title = re.search(r'(<title>(.*?)</title>)', htmlContent).groups()[1]
                # ERROR -> Title = re.search(r'name="Subject"\s+type="hidden"\s+value="([\w\(\)]+.*)"', htmlContent).groups()[0]

                #catServei = re.search(r'name="Serveis"\s+type="hidden"\s+value="(\w+.*)"', htmlContent).groups()[0]
                #catServeiPPS = re.search(r'name="Productes"\s+type="hidden"\s+value="(\w+.*)"', htmlContent).groups()[0]
                tinyContent = re.sub(r'^(.*?)(<script.*/script>)(.*?)(<applet.*/applet)(.*?)(<HEAD.*/HEAD>)(.*?)(<table.*<table.*/table>.*<table.*/table>.*/table>)(.*?)(.*?)<a\s*href="\/Upcnet\/Backoffice\/manualexp\.nsf\/\(\$All\)\?OpenView">.*$', r'\10', htmlContent, re.DOTALL | re.MULTILINE)

                object = self.createNotesObject('notesDocument', self.context, Title)
                object.setTitle(Title)
                object.setBody(tinyContent)
                object.setCreators(creator)
                object.setExcludeFromNav(True)
                #object.setCategory1(catServei)
                #object.setCategory2(catServeiPPS)
                object.reindexObject()

        logging.info('Done! End of Notes Migration process.')
        return 'OK, imported'

    def createNotesObject(self, type, folder, title):
        """
        """
        #import ipdb; ipdb.set_trace( )
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


# object.setBody,
# object.setExcludeFromNav,
# object.setCreationDate,
# object.setLocation,
# object.setCategory1,
# object.setExpirationDate,
# object.setCreators,
# object.setModificationDate,
# object.setCategory2,
# object.setFilename,
# object.setDefaultPage,
# object.setRelatedItems,
# object.setCategory3,
# object.setFormat,
# object.setDefaults,
# object.setRights,
# object.setCategory4,
# object.setId,
# object.setDescription,
# object.setSubject,
# object.setContentType,
# object.setLanguage,
# object.setEffectiveDate,
# object.setTitle,
# object.setContributors,
# object.setLayout
