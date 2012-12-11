"""Definition of the documentCSPT contenttype
"""
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from notes.kbtic.interfaces import IDocumentCSPT
from notes.kbtic.config import PROJECTNAME
from Products.ATVocabularyManager import NamedVocabulary

DocumentCSPTSchema = folder.ATFolderSchema.copy() + atapi.Schema((

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
                name='categoryCSPT',
                widget=atapi.InAndOutWidget(
                    format="select",
                    label_msgid='categoryCSPT_label',
                    description_msgid='categoryCSPT_help',
                    i18n_domain='notes.kbtic',
                ),
                languageIndependent=True,
                required=True,
                schemata="categorization",
                vocabulary=NamedVocabulary('categoryCSPT_keywords'),
                enforceVocabulary=True,
            ),

))

DocumentCSPTSchema['title'].storage = atapi.AnnotationStorage()
DocumentCSPTSchema['description'].storage = atapi.AnnotationStorage()

# Hide default category option
# DocumentCSPTSchema['subject'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
DocumentCSPTSchema['description'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
DocumentCSPTSchema['language'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
DocumentCSPTSchema['relatedItems'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
DocumentCSPTSchema['location'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}

schemata.finalizeATCTSchema(DocumentCSPTSchema, folderish=True, moveDiscussion=False)


class DocumentCSPT(folder.ATFolder):
    """Description of the documentCSPT"""
    implements(IDocumentCSPT)

    meta_type = "DocumentCSPT"
    schema = DocumentCSPTSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(DocumentCSPT, PROJECTNAME)
