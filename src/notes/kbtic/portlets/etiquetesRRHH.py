# -*- coding: utf-8 -*-

from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

#from zope.i18nmessageid import MessageFactory
#_ = MessageFactory('notes.kbtic')
from Products.CMFPlone import PloneMessageFactory as _


class IEtiquetesRRHHPortlet(IPortletDataProvider):
    """ Defines a new portlet
    """


class Assignment(base.Assignment):
    """ Assigner for portlet. """
    implements(IEtiquetesRRHHPortlet)
    title = _(u"Portlet Etiquetes RRHH", default=u'Portlet etiquetes RRHH')


class Renderer(base.Renderer):
    """ Overrides static.pt in the rendering of the portlet. """
    render = ViewPageTemplateFile('etiquetesRRHH.pt')

    def mostrarEtiquetesCategoryRRHH(self):
        """ Busca etiquetes dintre del portal_vocabulary segons idioma
        """
        urltool = getToolByName(self.context, 'portal_url')
        path = urltool.getPortalPath()

        results = []
        path = path + '/portal_vocabularies/categoryRRHH_keywords'
        keys = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm',
                                                             path={'query': path, 'depth': 1, },
                                                             sort_on='getObjPositionInParent')
        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
