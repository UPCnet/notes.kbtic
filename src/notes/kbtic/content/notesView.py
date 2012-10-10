# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class notesView(BrowserView):
    """ Default view for notesDocument objects
    """

    template = ViewPageTemplateFile('notesView.pt')

    def __call__(self):
        """
        """
        return self.template()

    def Categories(self):
        """ locate objects assigned to queried keyword
        """
        urltool = getToolByName(self.context, 'portal_url')
        path = '/'.join(urltool.absolute_url().split('/')[:-1]) + '/'

        results = []
        try:
            cat1 = self.context.category1
        except:
            cat1 = ()
        try:
            cat2 = self.context.category2
        except:
            cat2 = ()
        try:
            cat3 = self.context.category3
        except:
            cat3 = ()
        try:
            cat4 = self.context.categoryCSPT
        except:
            cat4 = ()

        objects = cat1 + cat2 + cat3 + cat4

        for value in objects:
            try:
                obj = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm', id=value)[0]

                results.append({'title': obj.Title,
                            'key': value,
                            'href': path + 'keywordsListing?' + value,
                            })
            except:
                # When an object is migrated, can come with keywords, but perhaps, doesn't exists still in Plone
                None

        return results
