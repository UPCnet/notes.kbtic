"""Definition of the documentRRHH contenttype
"""
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from notes.kbtic.interfaces import IDocumentRRHH
from notes.kbtic.config import PROJECTNAME
from Products.ATVocabularyManager import NamedVocabulary

DocumentRRHHSchema = folder.ATFolderSchema.copy() + atapi.Schema((

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
                name='categoryRRHH',
                widget=atapi.InAndOutWidget(
                    format="select",
                    label_msgid='categoryRRHH_label',
                    description_msgid='categoryRRHH_help',
                    i18n_domain='notes.kbtic',
                ),
                languageIndependent=True,
                required=True,
                schemata="categorization",
                vocabulary=NamedVocabulary('categoryRRHH_keywords'),
                enforceVocabulary=True,
            ),

))

DocumentRRHHSchema['title'].storage = atapi.AnnotationStorage()
DocumentRRHHSchema['description'].storage = atapi.AnnotationStorage()

# Hide default category option
DocumentRRHHSchema['subject'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
DocumentRRHHSchema['description'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
DocumentRRHHSchema['language'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
DocumentRRHHSchema['relatedItems'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
DocumentRRHHSchema['location'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}

schemata.finalizeATCTSchema(DocumentRRHHSchema, folderish=True, moveDiscussion=False)


class DocumentRRHH(folder.ATFolder):
    """Description of the documentRRHH"""
    implements(IDocumentRRHH)

    meta_type = "DocumentRRHH"
    schema = DocumentRRHHSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(DocumentRRHH, PROJECTNAME)
