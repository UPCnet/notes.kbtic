# -*- coding: utf-8 -*-
"""Definition of the NotesDocument contenttype
"""

from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from notes.kbtic.interfaces import INotesDocument
from notes.kbtic.config import PROJECTNAME
from Products.ATVocabularyManager import NamedVocabulary

NotesDocumentSchema = folder.ATFolderSchema.copy() + atapi.Schema((

            atapi.TextField(
                name='body',
                allowable_content_types=('text/plain',
                                               'text/structured',
                                               'text/html',),
                 default_output_type='text/x-html-safe',
                 widget=atapi.RichWidget(
                     label='Body',
                     label_msgid='label_body',
                     i18n_domain='notes.kbtic',
                     rows=40,
                 ),
             required=False,
             searchable=True,
             ),

            #CATEGORIES
            atapi.LinesField(
                name='category3',
                widget=atapi.InAndOutWidget(
                    format="select",
                    label='By Category',
                    description="Indica les categories de la vista (Notes - By Category) que té l'element",
                    label_msgid='category3_label',
                    description_msgid='category3_help',
                    i18n_domain='notes.kbtic',
                ),
                languageIndependent=True,
                multiValued=False,
                schemata="categorization",
                vocabulary=NamedVocabulary('category3_keywords'),
                enforceVocabulary=True,
            ),

            atapi.LinesField(
                name='category1',
                widget=atapi.InAndOutWidget(
                    format="select",
                    label='Categories per Servei',
                    description="Indicar totes les categories a les que pertany l'element",
                    label_msgid='category1_label',
                    description_msgid='category1_help',
                    i18n_domain='notes.kbtic',
                ),
                languageIndependent=True,
                required=False,
                schemata="categorization",
                vocabulary=NamedVocabulary('category1_keywords'),
                enforceVocabulary=True,
            ),

            atapi.LinesField(
                name='category2',
                widget=atapi.InAndOutWidget(
                    format="select",
                    label='Categories per Servei PPS',
                    description="Indicar totes les categories a les que pertany l'element",
                    label_msgid='category2_label',
                    description_msgid='category2_help',
                    i18n_domain='notes.kbtic',
                ),
                languageIndependent=True,
                required=False,
                schemata="categorization",
                vocabulary=NamedVocabulary('category2_keywords'),
                enforceVocabulary=True,
            ),

            atapi.LinesField(
                name='categoryADS',
                widget=atapi.InAndOutWidget(
                    format="select",
                    label='Categories By Category (per ADS-SPO)',
                    description="Indicar totes les categories a les que pertany l'element del tipus ADS-SPO",
                    label_msgid='category4_label',
                    description_msgid='category4_help',
                    i18n_domain='notes.kbtic',
                ),
                languageIndependent=True,
                required=False,
                schemata="categorization",
                vocabulary=NamedVocabulary('categoryADS_keywords'),
                enforceVocabulary=True,
            ),

))


NotesDocumentSchema['title'].storage = atapi.AnnotationStorage()
NotesDocumentSchema['description'].storage = atapi.AnnotationStorage()

# Hide default category option
# NotesDocumentSchema['subject'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
NotesDocumentSchema['description'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
NotesDocumentSchema['language'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
NotesDocumentSchema['relatedItems'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
NotesDocumentSchema['location'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}

schemata.finalizeATCTSchema(NotesDocumentSchema, folderish=True, moveDiscussion=False)


class NotesDocument(folder.ATFolder):
    """Description of the Example Type"""
    implements(INotesDocument)

    meta_type = "NotesDocument"
    schema = NotesDocumentSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(NotesDocument, PROJECTNAME)
