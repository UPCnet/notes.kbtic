# -*- coding: utf-8 -*-
import requests
import logging
import re

NOTES_USER = "******"
NOTES_PASS = "******"


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
                HTML = requests.get(match.string.split(' ')[5].replace('\n', ''), auth=('admin', 'admin')).content
                obj = self.context.portal_catalog.searchResults(portal_type='documentCSPT', id=match.string.split(' ')[5].replace('\n', '').split('/')[-1:])[0]
                newHTML = re.search(r'parent-fieldname-body">(.*?)div>(.*?)<div[^>]+id="category[^>]+class="documentByLine">(.*?)</div>(.*?)<div[^>]+id="portal-column-one"[^>]+class="cell width-1:4 position-0">(.*?)</html>', HTML, re.DOTALL | re.MULTILINE).groups()[1][:-20]
                import ipdb; ipdb.set_trace( )
                NotesUID = match.string.split(' ')[4].split('/')[-1:][0].replace('?OpenDocument','')
                replacedContent = re.sub('OpenDocument', 'ROBERTO', newHTML)
                objecte = obj.getObject()
                objecte.setBody(replacedContent)
                objecte.reindexObject()
                lista = lista + objecte.absolute_url() + '\n'
        
        return lista

# 2012-10-09 11:58:11 #6# Title: Actualizar el cliente de iPrint
# 2012-10-09 11:58:11 $6$ Notes: https://liszt.upc.es/C1256DA9004D37E9/2F2F551EB18D68B9852566D700413812/18ACDF538A0E2419C125799C00352390 Plone: http://gollum:8080/kbtic/import/actualizar-el-cliente-de-iprint-8
# 2012-10-09 11:58:12 #6# #Link: https://liszt.upc.es/Upcnet/Operacions/uses/CPST/Manualexplotacio.nsf/867962c7d68029f085256603006add59/5f00d25b1a244198c12573de003c7204?OpenDocument http://gollum:8080/kbtic/import/actualizar-el-cliente-de-iprint-8
# 2012-10-09 11:58:12 #6# Object migrated


# search Link
# replace "url other"
