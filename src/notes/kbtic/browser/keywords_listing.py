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
        keyword = self.request.environ['QUERY_STRING']
        objects1 = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                             sort_on='getObjPositionInParent',
                                                             category1=keyword)

        objects2 = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                             sort_on='getObjPositionInParent',
                                                             category2=keyword)

        objects3 = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                             sort_on='getObjPositionInParent',
                                                             category3=keyword)

        objects4 = self.context.portal_catalog.searchResults(portal_type='notesDocument',
                                                             sort_on='getObjPositionInParent',
                                                             category4=keyword)
        objects = objects1 + objects2 + objects3 + objects4

        for value in objects:
            results.append({'id': value.id,
                            'title': value.Title,
                            'url': value.getURL(),
                            'creator': value.Creator,
                            'creation_date': self.context.toLocalizedTime(value.CreationDate)})

        return results

    def keyword(self):
        """ from given keyword id return keyword title
        """
        keyword = self.request.environ['QUERY_STRING']

        obj = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', id=keyword)[0]

        return obj.Title
