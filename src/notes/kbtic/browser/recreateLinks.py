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
        'NomUsuari': '%s' % NOTES_USER
        }
        session.cookies.update(extra_cookies)
        response = session.post(LOGIN_URL, params, allow_redirects=True)
        cookie = {'Cookie': 'HabCookie=1; Desti=' + URL + '/' + PATH + '; RetornTancar=1; NomUsuari=' + NOTES_USER + ' LtpaToken=' + session.cookies['LtpaToken']}
        response = requests.get(MAIN_URL + PATH1, headers=cookie)

        linksFile = open('migrateCSPT.log', 'r')
        lista = " Objectes Modificats\n---------------------\n\n"
        for line in linksFile.readlines():
            match = re.search('#Link', line)
            if match is not None:
                try:
                    HTML = requests.get(match.string.split(' ')[5].replace('\n', ''), auth=('admin', 'admin')).content
                    obj = self.context.portal_catalog.searchResults(portal_type='documentCSPT', id=match.string.split(' ')[5].replace('\n', '').split('/')[-1:])[0]
                    newHTML = re.search(r'parent-fieldname-body">(.*?)div>(.*?)<div[^>]+id="category[^>]+class="documentByLine">(.*?)</div>(.*?)<div[^>]+id="portal-column-one"[^>]+class="cell width-1:4 position-0">(.*?)</html>', HTML, re.DOTALL | re.MULTILINE).groups()[1][:-20]
                    NotesUID = match.string.split(' ')[4].split('/')[-1:][0].replace('?OpenDocument', '').lower()
                    nouLink = self.searchNotesDoc(NotesUID)
                    url2search = '/' + '/'.join(match.string.split(' ')[4].split('/')[3:]).replace('?O', '\?\O')
                    newHTML = re.sub(r'<img\s+src="/icons/doclink.gif"\s+border="0"\s+alt="([\w\(\)]+.*?) />', nouLink, newHTML)
                    replacedContent = re.sub(url2search, nouLink, newHTML)
                    objecte = obj.getObject()
                    objecte.setBody(replacedContent)
                    objecte.reindexObject()
                    lista = lista + objecte.absolute_url() + '\n'
                except:
                    pass
        return lista

    def searchNotesDoc(self, uid):
        """ Search Plone Ids by Notes Ids
        """
        linksFile = open('migrateCSPT.log', 'r')
        for line in linksFile.readlines():
            match = re.search(uid.lower(), line.lower())
            if match is not None:
                return match.string.split(' ')[6].replace('\n', '')
