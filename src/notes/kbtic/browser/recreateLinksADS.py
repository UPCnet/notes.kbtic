# -*- coding: utf-8 -*-
import requests
import logging
import transaction
from pyquery import PyQuery as pq


class recreateLinks():

    def __call__(self):
        from datetime import datetime

        linksFileADS = open('/var/plone/kbtic.buildout/produccio/migrateADS.log', 'r')
        lista = " Objectes Modificats\n---------------------\n\n"
        changesFile = open('/var/plone/kbtic.buildout/produccio/linksreplacedADS.log', 'a')

        for line in linksFileADS:
            if "#Link" in line:
                link_intern = line.split(' ')[9].upper()

                # Si el link és a la mateixa DOCADS ho fem
                if "DOCADS.NSF" in link_intern:
                    HTML_PAGE_WITH_LINK = requests.get(str(line.split(' ')[7]), auth=('admin', '++++++++')).content
                    obj = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                                    path='/kbtic/ads-spo',
                                                                    id=line.split(' ')[7].replace('\n', '').split('/')[-1:])[0]
                    d = pq(HTML_PAGE_WITH_LINK)
                    try:
                        newHTML = d("#parent-fieldname-body").html()
                        change = "True"
                    except:
                        newHTML = HTML_PAGE_WITH_LINK
                        logging.info("## ERROR al editar content (no modificar...) ##")
                        change = "False"

                    if change == "True":
                        NotesUID2Search = link_intern.split('/')[-1:][0].replace('?OPENDOCUMENT', '').replace('\n', '')  # Esta en mays
                        titleLink, nouLink = self.searchNotesDocADS(NotesUID2Search)
                        url2search = ('/' + '/'.join(line.split(' ')[9].split('/')[3:])).replace('\n', '')
                        nouLink = '/' + '/'.join(nouLink.split('/')[4:])
                        replacedContent = newHTML.replace(url2search, nouLink)
                        replacedContent = replacedContent.replace('\r\n', '')
                        replacedContent = replacedContent.replace(("Database 'Documentació ADS i SPO', View 'By Category', Document '"), '')
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

                # Si el link és a KBTIC el fem
                elif "MANUALEXP.NSF" in link_intern:
                    # Agafem contingut html de la pàgina
                    HTML_PAGE_WITH_LINK = requests.get(str(line.split(' ')[7]), auth=('admin', '++++++++')).content
                    obj = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                                    path='/kbtic/ads-spo',
                                                                    id=line.split(' ')[7].replace('\n', '').split('/')[-1:])[0]
                    d = pq(HTML_PAGE_WITH_LINK)
                    try:
                        newHTML = d("#parent-fieldname-body").html()
                        change = "True"
                    except:
                        newHTML = HTML_PAGE_WITH_LINK
                        logging.info("## ERROR al editar content (no modificar...) ##")
                        change = "False"
                    if change == "True":
                        NotesUID2Search = link_intern.split('/')[-1:][0].replace('?OPENDOCUMENT', '').replace('\n', '')  # Esta en mays
                        titleLink, nouLink = self.searchNotesDocKBTIC(NotesUID2Search)
                        url2search = ('/' + '/'.join(line.split(' ')[9].split('/')[3:])).replace('\n', '')
                        nouLink = '/' + '/'.join(nouLink.split('/')[4:])
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

                # Sino, és extern i no el fem
                else:
                    original_plone_url = line.split(' ')[7]
                    changesFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'linkNOTModifiedIn (External): ' + link_intern.replace('\n', '') + ' in: ' + original_plone_url + '\n')
                    logging.info("linkNOTModifiedIn (External): %s in : %s", link_intern.replace('\n', ''), original_plone_url)

        changesFile.write('-----------------------------------------------------------------------------' + '\n')
        changesFile.write('                             END                                             ' + '\n')
        changesFile.write('-----------------------------------------------------------------------------' + '\n')
        changesFile.close()
        logging.info("END recreateLinksADS process!")
        return lista

    def searchNotesDocADS(self, uid):
        """ Search Plone Ids by Notes Ids
        """
        linksFile = open('/var/plone/kbtic.buildout/produccio/migrateADS.log', 'r')
        titleFile = open('/var/plone/kbtic.buildout/produccio/migrateADS.log', 'r')
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

    def searchNotesDocKBTIC(self, uid):
        """ Search Plone Ids by Notes Ids
        """
        linksFile = open('/var/plone/kbtic.buildout/produccio/migrateKBTIC.log', 'r')
        titleFile = open('/var/plone/kbtic.buildout/produccio/migrateKBTIC.log', 'r')
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

### EOF ###

