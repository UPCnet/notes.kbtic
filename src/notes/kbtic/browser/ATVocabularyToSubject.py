# -*- coding: utf-8 -*-
#
# 03 / November / 2014
# This file is used to migrate from ATVocabulary to Typical Plone subjects
# Categories --> Etiquetes
#

import logging
import csv
import os
import io
from datetime import datetime


class ATVocabularyToSubject():

    def __call__(self):
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filename='ATVocabularyToSubject.log',
                            level=logging.DEBUG)

        here = os.path.abspath(os.path.dirname(__file__))
        csvfile = os.path.join(here, 'newKeywords.csv')
        totalLines = len(list(csv.reader(open(csvfile))))
        log = open('MigrateToSubjects.log', mode='r+')  # GOLLUM
        log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Starting process. Total Objects: ' + str(totalLines) + '\n')
        logging.info('Starting process. Total Objects: %s', totalLines)

        keysADS = [result for result in self.context.uid_catalog.searchResults(portal_type='SimpleVocabularyTerm')
                   if 'categoryADS_keywords' in result.getPath()]

        keysRIN = [result for result in self.context.uid_catalog.searchResults(portal_type='SimpleVocabularyTerm')
                   if 'category3_keywords' in result.getPath()]

        keysServeis = [result for result in self.context.uid_catalog.searchResults(portal_type='SimpleVocabularyTerm')
                       if 'category1_keywords' in result.getPath()]

        with io.open(csvfile, 'r', encoding='iso-8859-1') as f:
            lines = f.readlines()[0:totalLines]  # all lines
            # lines = f.readlines()[0:2] # Testing lines
            num = 0
            for line in lines:
                num = num + 1
                lineData = line.split(',')
                starttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Processing line: ' + '\n')
                logging.info('Processing line: %s', line)
                if lineData[0] == 'By Category (ADS-SPO)':
                    # ADS-SPO --> categoryADS_keywords
                    if lineData[2] == '':
                        # No cal fer res --> assignació a empty
                        log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Nothing to do, empty destination category' + '\n')
                        logging.info('Nothing to do, empty destination category')
                        pass
                    else:

                        id_cat = ''
                        for value in keysADS:
                            if unicode(value.Title.decode('iso-8859-1')) == lineData[1] and 'categoryADS_keywords' in value.getPath():
                                id_cat = value.id
                                objects = self.context.portal_catalog.searchResults(portal_type='notesDocument', categoryADS=id_cat)
                                for obj in objects:
                                    actualKeys = obj.getObject().Subject()
                                    newKeys = lineData[2].encode('iso-8859-1')
                                    newlist = (list(actualKeys))
                                    newlist.append(newKeys)
                                    newlist = sorted(set(newlist), key=newlist.index)
                                    obj.getObject().edit(subject=newlist)
                                    log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Object: ' + str(obj.getPath()) + ' New Etiquetes: ' + str(newlist) + '\n')
                                    logging.info('Object: %s New Etiquetes: %s ', obj.getPath(), newlist)

                if lineData[0] == 'by Category (KBTIC-RIN)':
                    # KBTIC-RIN --> category3
                    if lineData[2] == '':
                        # No cal fer assignació a empty
                        log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Nothing to do, empty destination category' + '\n')
                        logging.info('Nothing to do, empty destination category')
                        pass
                    else:
                        id_cat = ''
                        for value in keysRIN:
                            if unicode(value.Title.decode('iso-8859-1')) == lineData[1] and 'category3_keywords' in value.getPath():
                                id_cat = value.id
                                objects = self.context.portal_catalog.searchResults(portal_type='notesDocument', category3=id_cat)
                                for obj in objects:
                                    actualKeys = obj.getObject().Subject()
                                    newKeys = lineData[2].encode('iso-8859-1')
                                    newlist = (list(actualKeys))
                                    newlist.append(newKeys)
                                    newlist = sorted(set(newlist), key=newlist.index)
                                    obj.getObject().edit(subject=newlist)
                                    log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Object: ' + str(obj.getPath()) + ' New Etiquetes: ' + str(newlist) + '\n')
                                    logging.info('Object: %s New Etiquetes: %s ', obj.getPath(), newlist)
                if lineData[0] == 'Categories servei':
                    # Categories Servei --> category1
                    if lineData[2] == '':
                        # No cal fer assignació a empty
                        log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Nothing to do, empty destination category' + '\n')
                        logging.info('Nothing to do, empty destination category')
                        pass
                    else:
                        id_cat = ''
                        for value in keysServeis:
                            if unicode(value.Title.decode('iso-8859-1')) == lineData[1] and 'category1_keywords' in value.getPath():
                                id_cat = value.id
                                objects = self.context.portal_catalog.searchResults(portal_type='notesDocument', category1=id_cat)
                                for obj in objects:
                                    actualKeys = obj.getObject().Subject()
                                    newKeys = lineData[2].encode('iso-8859-1')
                                    newlist = (list(actualKeys))
                                    newlist.append(newKeys)
                                    newlist = sorted(set(newlist), key=newlist.index)
                                    obj.getObject().edit(subject=newlist)
                                    log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'Object: ' + str(obj.getPath()) + ' New Etiquetes: ' + str(newlist) + '\n')
                                    logging.info('Object: %s New Etiquetes: %s ', obj.getPath(), newlist)
        endtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + 'End process. Started at: ' + starttime + ' Ended at: ' + endtime + '\n')
        logging.info('End process.  Started at: %s Ended at: %s', starttime, endtime)
        f.close()
        return "WELL DONE! Start time: " + starttime + " End time: " + endtime

# ### EOF ###
