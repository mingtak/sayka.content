# -*- coding: utf-8 -*-
from sayka.content import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
import logging

logger = logging.getLogger("Custom.css")


class CustomCSS(BrowserView):
    """ Backend.css """

    template = ViewPageTemplateFile("template/custom_css.pt")


    def __call__(self):
        portal = api.portal.get()
        context = self.context
        request = self.request

        alsoProvides(request, IDisableCSRFProtection)

        css = request.form.get('css')
        if css:
            with open('/home/henryc/sayka/zeocluster/src/sayka.theme/src/sayka/theme/theme/css/custom.css', 'w') as file:
                file.write(css)
                api.portal.show_message('Override css file finish.', request=request, type='info')
                request.response.redirect('%s/@@custom_css' % portal.absolute_url())

                return
        else:
            with open('/home/henryc/sayka/zeocluster/src/sayka.theme/src/sayka/theme/theme/css/custom.css') as file:
                self.css = file.read()
                return self.template()

