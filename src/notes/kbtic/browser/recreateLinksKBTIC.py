# -*- coding: utf-8 -*-
import requests
import logging
import re

NOTES_USER = ""
NOTES_PASS = ""


class recreateLinks():

    def __call__(self):
        ###
        ###

        session = requests.session()

        URL = 'https://liszt.upc.es'
        LOGIN_URL = 'https://liszt.upc.es/names.nsf?Login'
        PATH1 = '2F2F551EB18D68B9852566D700413812'
        PATH = 'C1256DA9004D37E9/' + PATH1
        BASE_URL = 'https://liszt.upc.es/%s' % PATH
        TRAVERSE_PATH = '/Upcnet/Operacions/uses/CPST/Manualexplotacio.nsf/'
        MAIN_URL = 'https://liszt.upc.es' + TRAVERSE_PATH + '?ReadViewEntries&ExpandView'

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
                    'NomUsuari': '%s' % NOTES_USER,
                    'LtpaToken': 'AAECAzUwQjhBQjBCNTBCOEMwMjNDTj1Vc3VhcmkgRWxlbmE2L089VXBjbmV0FDmzA8JKM1b4+yNX6GIlAGrpzII='
        }
        session.cookies.update(extra_cookies)
        response = session.post(LOGIN_URL, params, allow_redirects=True)
        cookie = {'Cookie': 'HabCookie=1; Desti=' + URL + '/' + PATH + '; RetornTancar=1; NomUsuari=' + NOTES_USER + ' LtpaToken=' + session.cookies['LtpaToken']}
        response = requests.get(MAIN_URL + PATH1, headers=cookie)

        linksFile = open('migrateKBTIC.log', 'r')
        lista = " Objectes Modificats\n---------------------\n\n"

#'2012-11-30
#09:47:36
#156#
#Link:
#ORIGINAL_NOTES_PATH:
#https://liszt.upc.es/Upcnet/Backoffice/manualexp.nsf/626E6035EADBB4CD85256499006B15A6/53ED94AE4C56BD78C12579EA005757A9
#ORIGINAL_PLONE_URL:
#http://gollum:11005/kbtic/kbtic-rin/bo-aps-tasques-ads-periodiques
#LINK_TO:
#https://liszt.upc.es/Upcnet/Backoffice/manualexp.nsf/bf25ab0f47ba5dd785256499006b15a4/899dfb2802c855f2c12578bc003e8b13?OpenDocument\n'

        for line in linksFile:

            if "#Link" in line:  # Tenim el link
                link_intern = line.split(' ')[9].upper()
                if "MANUALEXP.NSF" in link_intern:  # Mirem si es link a mateixa BBDD
                    # Agafem contingut html de la
                    HTML_PAGE_WITH_LINK = requests.get(str(line.split(' ')[7]), auth=('admin', 'admin')).content
                    obj = self.context.portal_catalog.searchResults(portal_type='notesDocument', id=line.split(' ')[7].replace('\n', '').split('/')[-1:])[0]
                    # check next line
                    newHTML = re.search(r'parent-fieldname-body">(.*?)div>(.*?)<div[^>]+id="category[^>]+class="documentByLine">(.*?)</div>(.*?)<div[^>]+id="portal-column-one"[^>]+class="cell width-1:4 position-0">(.*?)</html>', HTML_PAGE_WITH_LINK, re.DOTALL | re.MULTILINE).groups()[1][:-20]
                    NotesUID2Search = link_intern.split('/')[-1:][0].replace('?OPENDOCUMENT', '').replace('\n','')  # Esta en mays
                    nouLink = self.searchNotesDoc(NotesUID)
                    url2search = '/' + '/'.join(match.string.split(' ')[4].split('/')[3:]).replace('?O', '\?\O')
                    newHTML = re.sub(r'<img\s+src="/icons/doclink.gif"\s+border="0"\s+alt="([\w\(\)]+.*?) />', nouLink, newHTML)
                    replacedContent = re.sub(url2search, nouLink, newHTML)
                    objecte = obj.getObject()
                    objecte.setBody(replacedContent)
                    objecte.reindexObject()
                    lista = lista + objecte.absolute_url() + '\n'
                else:  # Sino, es un link extern
                    original_plone_url = line.split(' ')[7]
                    print ("Link_extern: %s in doc: %s", link_intern, original_plone_url)
        return lista

    def searchNotesDoc(self, uid):
        """ Search Plone Ids by Notes Ids
        """
        linksFile = open('migrateKBTIC.log', 'r')
        for line in linksFile:
            # Mirem si UID in origin_url
            if uid in line.split(' ')[5].upper:
                return line.split(' ')[7].replace('\n', '')
