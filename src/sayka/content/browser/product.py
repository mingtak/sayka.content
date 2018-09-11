from sayka.content import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

class ProductView(BrowserView):
    template = ViewPageTemplateFile('template/product_view.pt')
    def __call__(self):
        request = self.request
        context = self.context
        portal = api.portal.get()

        result = api.content.find(context=portal['shopping_listing'], portal_type="Product"
            ,sort_on='created', sort_order='descending', sort_limit=8)
        self.result = result
        count = 0
        for i in range(1, 9):
            if getattr(context, 'image_%s' %(i)):
                count += 1
        self.count = count
        return self.template()


class ShoppingList(BrowserView):
    template = ViewPageTemplateFile('template/shopping_list.pt')
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        return self.template()
