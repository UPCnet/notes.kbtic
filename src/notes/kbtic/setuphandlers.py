# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_TITLE
from Products.CMFPlone.utils import _createObjectByType
from DateTime import DateTime
from plone.app.controlpanel.mail import IMailSchema
from Products.CMFPlone import PloneMessageFactory as _


def setupVarious(context):
    if context.readDataFile('notes.kbtic_various.txt') is None:
        return
    portal = context.getSite()

    # permetre @. als usernames
    portal.portal_registration.manage_editIDPattern('^[A-Za-z][A-Za-z0-9_\-@.]*$')
    #definir el layout de la pagina principal
    #portal.setLayout('homepage')

    # configurem mail
    mail = IMailSchema(portal)
    mail.smtp_host = u'localhost'
    mail.email_from_name = "Administrador Web"
    mail.email_from_address = "noreply@localhost.cat"

    # Vocabularis del lloc
    voctool = getToolByName(portal, 'portal_vocabularies')
    try:
        category1_keywords = _createObjectByType('SortedSimpleVocabulary', voctool, 'category1_keywords')
        keywords = [
                    (u"cat01_key1", u"10100-00 Atenció a  l'usuari"),
                    (u"cat02_key1", u"10101-00 Correcció exàmens ICE"),
                    (u"cat03_key1", u"10200-00 Resolució de consultes ofimàtiques"),
                    (u"cat04_key1", u"10300-00 Correu electrònic"),
                    (u"cat05_key1", u"10301-00 Correu electrònic DN"),
                    (u"cat06_key1", u"10302-00 Correu electrònic K2"),
                    (u"cat07_key1", u"10303-00 Relay i gestió de dominis de correu"),
                    (u"cat08_key1", u"10304-00 Llistes de distribució de correu"),
                    (u"cat09_key1", u"10312-00 Agenda K2"),
                    (u"cat10_key1", u"10350-00 Missatgeria instantània"),
                    (u"cat11_key1", u"10400-00 Impressió en xarxa"),
                    (u"cat12_key1", u"10500-00 Repositori de fitxers"),
                    (u"cat13_key1", u"10501-00 Repositori de fitxers personals"),
                    (u"cat14_key1", u"10502-00 Repositori de fitxers de grup"),
                    (u"cat15_key1", u"10600-00 Gestió d'estacions de treball personals"),
                    (u"cat16_key1", u"10610-00 Configuració mantinguda de software"),
                    (u"cat17_key1", u"10611-00 Configuració mantinguda de software - entorn Windows"),
                    (u"cat18_key1", u"10612-00 Configuració mantinguda de software - entorn Linux"),
                    (u"cat19_key1", u"10612-01 Configuració PUB-Linux (SBD)"),
                    (u"cat20_key1", u"10620-00 Instal·lació de software"),
                    (u"cat21_key1", u"10700-00 Aules informàtiques"),
                    (u"cat22_key1", u"10900-00 Dispositius mòbils"),
                    (u"cat23_key1", u"10900-10 Blackberry DN (còpia per corregir imputacions SIT)"),
                    (u"cat24_key1", u"10910-00 Blackberry DN"),
                    (u"cat25_key1", u"11000-00 Bases de dades bibliogràfiques en CD-ROM"),
                     ]
        for keyword in keywords:
            object = _createObjectByType('SimpleVocabularyTerm', category1_keywords, keyword[0])
            object.setTitle(keyword[1])
            object.reindexObject()
    except:
        pass

    #paraules clau de persones
    try:
        category2_keywords = _createObjectByType('SortedSimpleVocabulary', voctool, 'category2_keywords')
        keywords = [(u"cat2_key1", u"Cat2 Key1"),
                    (u"cat2_key2", u"Cat2 Key2"),
                       ]
        for keyword in keywords:
            object = _createObjectByType('SimpleVocabularyTerm', category2_keywords, keyword[0])
            object.setTitle(keyword[1])
            object.reindexObject()
    except:
        pass

    #paraules clau de barris
    try:
        category3_keywords = _createObjectByType('SortedSimpleVocabulary', voctool, 'category3_keywords')
        keywords = [(u"cat3_key1", u"Cat3 Key1"),
                    (u"cat3_key2", u"Cat3 Key2"),
                    ]
        for keyword in keywords:
            object = _createObjectByType('SimpleVocabularyTerm', category3_keywords, keyword[0])
            object.setTitle(keyword[1])
            object.reindexObject()
    except:
        pass

    #paraules clau de xifres
    try:
        category4_keywords = _createObjectByType('SortedSimpleVocabulary', voctool, 'category4_keywords')
        keywords = [(u"cat4_key1", u"Cat4 Key1"),
                    (u"cat4_key2", u"Cat4 Key2"),
                    ]
        for keyword in keywords:
            object = _createObjectByType('SimpleVocabularyTerm', category4_keywords, keyword[0])
            object.setTitle(keyword[1])
            object.reindexObject()
    except:
        pass

    portal.setTitle("Portal Notes")

    langtool = getToolByName(portal, 'portal_languages')
    langtool.manage_setLanguageSettings(defaultLanguage='ca',
                                        supportedLanguages=['ca', 'es', 'en'],
                                        setUseCombinedLanguageCodes=0,
                                        setForcelanguageUrls=0,
                                        setPathN=1,
                                        setCookieN=1,
                                        setAllowContentLanguageFallback=0,
                                        setRequestN=0,
                                        startNeutral=1,
                                        displayFlags=False)
