# -*- coding: utf-8 -*-
import requests
import logging
import re
import transaction
from pyquery import PyQuery as pq


NOTES_USER = ""
NOTES_PASS = ""


class recreateLinks():

    def __call__(self):
        from datetime import datetime

        linksFile = open('migrateKBTIC.log', 'r')
        lista = " Objectes Modificats\n---------------------\n\n"
        changesFile = open('linksreplacedKBTIC.log', 'a')
        num_error = 0
        for line in linksFile:
            if "#Link" in line:
                link_intern = line.split(' ')[9].upper()
                if "MANUALEXP.NSF" in link_intern:  # Mirem si es link a mateixa BBDD
                    # Agafem contingut html de la pàgina
                    HTML_PAGE_WITH_LINK = requests.get(str(line.split(' ')[7]), auth=('admin', '++++++++')).content
                    obj = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                                    path='/kbtic/kbtic-rin',
                                                                    id=line.split(' ')[7].replace('\n', '').split('/')[-1:])[0]
                    d = pq(HTML_PAGE_WITH_LINK)
                    try:
                        newHTML = d("#parent-fieldname-body").html()
                        change = "True"
                    except:
                        newHTML = HTML_PAGE_WITH_LINK
                        num_error = num_error + 1
                        logging.info("## ERROR al editar content (no modificar...)##")
                        change = "False"
                    # try:
                    #     newHTML = re.search(r'parent-fieldname-body">(.*?)viewlet-below-content-body">', HTML_PAGE_WITH_LINK, re.DOTALL | re.MULTILINE).groups()[0][:-100]
                    # except:
                    #     newHTML = HTML_PAGE_WITH_LINK
                    #     logging.info("----------- ERROR: Content corrupte. Es deixa com estava...: %s ", obj.absolute_url())
                    if change == "True":
                        NotesUID2Search = link_intern.split('/')[-1:][0].replace('?OPENDOCUMENT', '').replace('\n', '')  # Esta en mays
                        titleLink, nouLink = self.searchNotesDoc(NotesUID2Search)
                        url2search = ('/' + '/'.join(line.split(' ')[9].split('/')[3:])).replace('\n', '')
                        nouLink = '/' + '/'.join(nouLink.split('/')[3:])
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
                        changesFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'linkModifiedIn: ' + objecte.absolute_url() + '\n')
                        logging.info("linkModifiedIn: %s ", objecte.absolute_url())
                        lista = lista + objecte.absolute_url() + '\n'
                        change = "False"
                    else:
                        logging.info("## ERROR al editar content (no modificar): %s", obj.getObject().absolute_url())
                        change = "True"
                else:  # Sino, es un link extern no el fem...
                    original_plone_url = line.split(' ')[7]
                    changesFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'linkNOTModifiedIn (External): ' + link_intern.replace('\n', '') + ' in: ' + original_plone_url + '\n')
                    logging.info("linkNOTModifiedIn (External): %s in : %s", link_intern.replace('\n', ''), original_plone_url)
        changesFile.write('-----------------------------------------------------------------------------' + '\n')
        changesFile.write('                             END: ' + str(num_error) + ' errores' + '\n')
        changesFile.write('-----------------------------------------------------------------------------' + '\n')
        changesFile.close()
        logging.info("END recreateLinksKBTIC process!")
        return lista

    def searchNotesDoc(self, uid):
        """ Search Plone Ids by Notes Ids
        """
        linksFile = open('migrateKBTIC.log', 'r')
        titleFile = open('migrateKBTIC.log', 'r')
        value = ''
        title = ''
        for line in linksFile:
            # Mirem si UID in origin_url
            if uid in line:
                value = line.split(' ')[6].replace('\n', '')
                titleLine = line.split(' ')[2].replace('$', '#')
                for startline in titleFile:
                    if titleLine in startline:
                        title = (' '.join(startline.split(' ')[4:])).replace('\n', '')
                        return (title, value)
        if value == '':
            value = '[Document-Notes-No-Trobat]'
        return (title, value)

