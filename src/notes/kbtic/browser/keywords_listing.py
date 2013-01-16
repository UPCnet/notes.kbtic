# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView


class KeywordsView(BrowserView):

    template = ViewPageTemplateFile('keywords_listing.pt')

    def __call__(self):
        """
        """
        return self.template()

    def objectsByKey(self):
        """ locate objects assigned to queried keyword
        """
        results = []
        
        # Search in root (all object) or in context only (ads or kbtic)
        if len(self.context.getPhysicalPath())>2:
            search_path = '/'.join(self.context.getPhysicalPath()[0:3])
        else: 
            search_path = '/'.join(self.context.getPhysicalPath())

        keyword = self.request.environ['QUERY_STRING']
        objects1 = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                             sort_on='getObjPositionInParent',
                                                             path = search_path,
                                                             category1=keyword)

        objects2 = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                             sort_on='getObjPositionInParent',
                                                             path = search_path,                                                             
                                                             category2=keyword)

        objects3 = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                             sort_on='getObjPositionInParent',
                                                             path = search_path,                                                             
                                                             category3=keyword)

        objects4 = self.context.portal_catalog.searchResults(portal_type='documentCSPT',
                                                             sort_on='getObjPositionInParent',
                                                             path = search_path,                                                             
                                                             categoryCSPT=keyword)

        objects5 = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                             sort_on='getObjPositionInParent',
                                                             path = search_path,                                                             
                                                             categoryADS=keyword)        

        objects = objects1 + objects2 + objects3 + objects4 + objects5 

        for value in objects:
            results.append({'id': value.id,
                            'title': value.Title,
                            'url': value.getURL(),
                            'creator': str((value.Creator).lower()).replace('/upcnet', '').replace(' ', '.'),
                            'review_state': value.review_state,
                            'creation_date': self.context.toLocalizedTime(value.CreationDate),
                            'modification_date': self.context.toLocalizedTime(value.ModificationDate)})

        return results

    def keyword(self):
        """ from given keyword id return keyword title
        """
        keyword = self.request.environ['QUERY_STRING']

        try:
            obj = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', id=keyword)[0]
            value = obj.Title
        except:
            value = "Paraula clau no trobada"

        return value

