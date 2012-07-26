"""Definition of the NotesDocument contenttype
"""
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from notes.kbtic.interfaces import INotesDocument
from notes.kbtic.config import PROJECTNAME
from Products.ATVocabularyManager import NamedVocabulary

NotesDocumentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

     atapi.TextField(name='body',
            searchable=1,
            required=1,
            allowable_content_types=('text/plain',
                                       'text/structured',
                                       'text/html',),
            default_output_type='text/x-html-safe',
            widget=atapi.RichWidget(label_msgid='label_missatge',
                                      i18n_domain='ajuntament.core',
                                      rows=20,),
           ),

            #CATEGORIES
            atapi.LinesField(
                name='category1',
                widget=atapi.InAndOutWidget(
                    format="select",
                    label_msgid='category1_label',
                    description_msgid='category1_help',
                    i18n_domain='ajuntament.core',
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
                    label_msgid='category2_label',
                    description_msgid='category2_help',
                    i18n_domain='ajuntament.core',
                ),
                languageIndependent=True,
                multiValued=False,
                schemata="categorization",
                vocabulary=NamedVocabulary('category2_keywords'),
                enforceVocabulary=True,
            ),

            atapi.LinesField(
                name='category3',
                widget=atapi.InAndOutWidget(
                    format="select",
                    label_msgid='category3_label',
                    description_msgid='category3_help',
                    i18n_domain='ajuntament.core',
                ),
                languageIndependent=True,
                multiValued=False,
                schemata="categorization",
                vocabulary=NamedVocabulary('category3_keywords'),
                enforceVocabulary=True,
            ),

            atapi.LinesField(
                name='category4',
                widget=atapi.InAndOutWidget(
                    format="select",
                    label_msgid='category4_label',
                    description_msgid='category4_help',
                    i18n_domain='ajuntament.core',
                ),
                languageIndependent=True,
                multiValued=False,
                schemata="categorization",
                vocabulary=NamedVocabulary('category4_keywords'),
                enforceVocabulary=True,
            ),


))


NotesDocumentSchema['title'].storage = atapi.AnnotationStorage()
NotesDocumentSchema['description'].storage = atapi.AnnotationStorage()

# Hide default category option
NotesDocumentSchema['subject'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
NotesDocumentSchema['description'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
NotesDocumentSchema['language'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
NotesDocumentSchema['relatedItems'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
NotesDocumentSchema['location'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}

schemata.finalizeATCTSchema(NotesDocumentSchema, moveDiscussion=False)


class NotesDocument(base.ATCTContent):
    """Description of the Example Type"""
    implements(INotesDocument)

    meta_type = "NotesDocument"
    schema = NotesDocumentSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(NotesDocument, PROJECTNAME)
