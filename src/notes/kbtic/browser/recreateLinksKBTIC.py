# -*- coding: utf-8 -*-
import requests
import logging
import re
import transaction

NOTES_USER = ""
NOTES_PASS = ""


class recreateLinks():

    def __call__(self):
        linksFile = open('migrateKBTIC.log', 'r')
        lista = " Objectes Modificats\n---------------------\n\n"
        changesFile = open('linksreplaced.log', 'a')

        for line in linksFile:
            if "#Link" in line:
                link_intern = line.split(' ')[9].upper()
                if "MANUALEXP.NSF" in link_intern:  # Mirem si es link a mateixa BBDD
                    # Agafem contingut html de la pàgina
                    HTML_PAGE_WITH_LINK = requests.get(str(line.split(' ')[7]), auth=('admin', 'admin')).content
                    obj = self.context.portal_catalog.searchResults(portal_type='notesDocument', path='/kbtic/kbtic-rin', id=line.split(' ')[7].replace('\n', '').split('/')[-1:])[0]
                    # check next line
                    # newHTML = re.search(r'parent-fieldname-body">(.*?)div>(.*?)<div[^>]+id="category[^>]+class="documentByLine">(.*?)</div>(.*?)<div[^>]+id="portal-column-one"[^>]+class="cell width-1:4 position-0">(.*?)</html>', HTML_PAGE_WITH_LINK, re.DOTALL | re.MULTILINE).groups()[1][:-20]

                    # if 'gestor-de-serveis-cspt-centre-sanitari-parc-tauli' in str(line.split(' ')[7]):
                    #     import ipdb;ipdb.set_trace()
                    # antes newHTML = re.search(r'parent-fieldname-body">(.*?)div>(.*?)viewlet-below-content-body">(.*?)</html>', HTML_PAGE_WITH_LINK, re.DOTALL | re.MULTILINE).groups()[1][:-39]
                    # if 'sirena-protocol-atencio-avaries-dispositius' in line:
                    #     import ipdb;ipdb.set_trace()
                    newHTML = re.search(r'parent-fieldname-body">(.*?)viewlet-below-content-body">', HTML_PAGE_WITH_LINK, re.DOTALL | re.MULTILINE).groups()[0][:-100]
                    NotesUID2Search = link_intern.split('/')[-1:][0].replace('?OPENDOCUMENT', '').replace('\n', '')  # Esta en mays
                    titleLink, nouLink = self.searchNotesDoc(NotesUID2Search)
                    url2search = ('/' + '/'.join(line.split(' ')[9].split('/')[3:])).replace('\n', '')
                    #newHTML = re.sub(r'<img\s+src="/icons/doclink.gif"\s+border="0"\s+alt="([\w\(\)]+.*?) />', nouLink, newHTML)
                    replacedContent = newHTML.replace(url2search, nouLink)
                    replacedContent = replacedContent.replace('\r\n', '')
                    replacedContent = replacedContent.replace(("Database 'KBTIC - RIN', View 'By Category', Document '"), '')
                    replacedContent = replacedContent.replace("/icons/ecblank.gif", '/++resource++notes_kbtic_images/ecblank.gif')
                    replacedContent = replacedContent.replace("/icons/doclink.gif", '/++resource++notes_kbtic_images/doclink.gif')
                    replacedContent = replacedContent.replace("/icons/collapse.gif", '/++resource++notes_kbtic_images/collapse.gif')
                    replacedContent = replacedContent.replace('alt="ecblank.gif"', "")
                    replacedContent = replacedContent.replace('title="doclink.gif"', "")
                    objecte = obj.getObject()
                    objecte.setBody(replacedContent)
                    objecte.indexObject()
                    transaction.commit()
                    changesFile.write('Url changed in ' + objecte.absolute_url() + '\n')
                    lista = lista + objecte.absolute_url() + '\n'
                else:  # Sino, es un link extern no el fem...
                    original_plone_url = line.split(' ')[7]
                    changesFile.write('External_LINK: ' + link_intern.replace('\n', '') + ' in doc: ' + original_plone_url + '\n')
                    #logging.info("External_LINK: %s in doc: %s", link_intern.replace('\n', ''), original_plone_url)
        changesFile.write('-----------------------------------------------------------------------------' + '\n')
        changesFile.write('                             END                                             ' + '\n')
        changesFile.write('-----------------------------------------------------------------------------' + '\n')
        changesFile.close()
        logging.info("END recreateLinksKBTIC process!")
        return lista

    def searchNotesDoc(self, uid):
        """ Search Plone Ids by Notes Ids
        """
        linksFile = open('fakeKBTIC.log', 'r')
        titleFile = open('fakeKBTIC.log', 'r')
        value = ''
        title = ''
        for line in linksFile:
            # Mirem si UID in origin_url
            if uid in line:
                #import ipdb;ipdb.set_trace()
                value = line.split(' ')[6].replace('\n', '')
                titleLine = line.split(' ')[2].replace('$', '#')
                for startline in titleFile:
                    if titleLine in startline:
                        title = (' '.join(startline.split(' ')[4:])).replace('\n', '')
                        return (title, value)
        if value == '':
            value = '[Document-Notes-No-Trobat]'
        return (title, value)
