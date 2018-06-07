# -*- coding: utf-8 -*-
from sayka.content import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import json


class CartUpdate(BrowserView):
    def __call__(self):
        request = self.request
        action = request.get('action')
        item_id = request.get('item_id')
        
        shopCart = request.cookies.get('shopCart', [])
        if shopCart:
            shopCart = json.loads(shopCart)
        else:
            shopCart = []

        if action == 'add':
            if self.checkExist(shopCart, item_id) is None:
                shopCart.append([item_id, 1])
                request.response.setCookie('shopCart', json.dumps(shopCart), path="/")
                return 'Add Success'
            else:
                return 'Item exist'

        elif action == 'del':
            index = self.checkExist(shopCart, item_id)
            if index is not None:
                shopCart.pop(index)
                request.response.setCookie('shopCart', json.dumps(shopCart), path="/")
                return 'remove success'
        elif action == 'update':
            index = self.checkExist(shopCart, item_id)
            if index is not None:
                number = request.get('number')
                shopCart[index][1] = int(number)
                request.response.setCookie('shopCart', json.dumps(shopCart), path="/")
		total_price = 0
		for item in shopCart:
		    sale_price = api.content.find(id=item[0])[0].getObject().sale_price
		    total_price += sale_price * item[1]
                return total_price

    def checkExist(self, shopCart, item_id):
        for item in shopCart:
            if item_id == item[0]:
                return shopCart.index(item)
        return None
