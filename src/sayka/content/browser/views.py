# -*- coding: utf-8 -*-
from sayka.content import _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import json
from db.connect.browser.views import SqlObj
from Products.CMFPlone.utils import safe_unicode
from datetime import datetime
import time


class ConfirmCart(BrowserView):
    template = ViewPageTemplateFile('template/confirm_cart.pt')
    def __call__(self):
        request = self.request
        abs_url = api.portal.get().absolute_url()
        shopCart = request.cookies.get('shopCart', [])
        shopCart = json.loads(shopCart)
        if not shopCart:
            request.response.redirect('%s/shopping_listing' %abs_url)
        if api.user.is_anonymous():
            request.response.redirect('%s/login' %abs_url)
            api.portal.show_message(message='請先登入', request=request,type='warn')
            return
        self.shopCart = shopCart
    	total_price = 0

    	for item in shopCart:
	        content = api.content.find(id=item[0])
	        sale_price = content[0].getObject().sale_price
	        total_price += sale_price * item[1]
        self.total_price = total_price
        return self.template()


class UpdateDist(BrowserView):
    def __call__(self):
        configStr = 'allpay.content.browser.allpaySetting.IAllpaySetting'
        addr = self.request.get('address')
        distList = api.portal.get_registry_record('%s.distList' % configStr)
        dist = distList.split(safe_unicode(addr))[1].split(':')[1].split('|')
        data = {}
        for item in dist:
            try:
                road = item.split('\r\n')[0].split(',')[0]
                number = item.split('\r\n')[0].split(',')[1]
                data[road] = number
            except:
                import pdb;pdb.set_trace()
        return json.dumps(data)


class Billing(BrowserView):
    template = ViewPageTemplateFile("template/billing.pt")
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect(api.portal.get().absolute_url())
            api.portal.show_message('%s' % '請先登入'.decode('utf-8'), self.request, 'error')
            return
        context = self.context
        request = self.request
        portal = api.portal.get()
        configStr = 'allpay.content.browser.allpaySetting.IAllpaySetting'
        shopCart = request.cookies.get('shopCart', '[]')
        self.cart = json.loads(shopCart)
        if not self.cart:
            self.request.response.redirect(api.portal.get().absolute_url())
            api.portal.show_message('%s' % '您目前無商品無法結帳'.decode('utf-8'), self.request, 'error')
            return
        
        city = api.portal.get_registry_record('%s.citySorted' % configStr)
        self.city = city.split(',')

        user = api.user.get_current()

        self.user_name = user.getProperty('fullname', '')
        self.user_email = user.getProperty('email', '')
        self.user_city = user.getProperty('city', '')
        self.user_district = user.getProperty('district', '')
        self.user_zip = user.getProperty('zip', '')
        self.user_address = user.getProperty('address', '')
        self.user_phoneNo = user.getProperty('phoneNo', '')
        self.user_cellNo = user.getProperty('cellNo', '')

        distList = api.portal.get_registry_record('%s.distList' % configStr)
        user_dist_list = []
        if self.user_city:
            user_dist_set = distList.split(safe_unicode(self.user_city))[1].split(':')[1].split('|')
            for item in user_dist_set:
                road = item.split('\r\n')[0].split(',')[0]
                number = item.split('\r\n')[0].split(',')[1]
                user_dist_list.append([road, number])

        self.user_dist_list = user_dist_list

        return self.template()


class CheckProfile(BrowserView):
    def __call__(self):

        if 'Manager' in api.user.get_roles():
            self.request.response.redirect(api.portal.get().absolute_url())
            return

        execSql = SqlObj()

        request = self.request
        buyer_city = request.get('buyer_city')
        buyer_district = request.get('buyer_district')
        buyer_zip = request.get('buyer_zip')
        buyer_cellNo= request.get('buyer_cellNo')
        buyer_phoneNo = request.get('buyer_phoneNo')
        buyer_name = request.get('buyer_name')
        buyer_email = request.get('buyer_email')
        buyer_address = request.get('buyer_address')

        invoice_code = request.get('invoice_code', '')
        invoice_name = request.get('invoice_name', '')
        invoice_type = request.get('invoice_type', '')

        user_id = api.user.get_current().getUserId()
        user_name = api.user.get_current().getUserName()
        user = api.user.get(user_name)

        execStr = """SELECT id FROM invoice_set WHERE user_id = '{}' AND
            invoice_name = '{}' AND invoice_code = '{}' AND invoice_type = '{}'
            """.format(user_id, invoice_name, invoice_code, invoice_type)
        invoice_result = execSql.execSql(execStr)
        if not invoice_result:
            # 寫進發票的常用資料庫
            execStr = """INSERT INTO invoice_set(user_id,invoice_name, invoice_code, invoice_type) 
                VALUES('{}','{}','{}','{}')""".format(user_id, invoice_name, invoice_code, invoice_type)
            execSql.execSql(execStr)
            # 抓剛剛寫進的id
            execStr = """SELECT id FROM invoice_set WHERE user_id = '{}' AND
                invoice_name = '{}' AND invoice_code = '{}' AND invoice_type = '{}'
                """.format(user_id, invoice_name, invoice_code, invoice_type)
            invoice_result = execSql.execSql(execStr)


        execStr = """SELECT id FROM buyer_set WHERE user_id = '{}' AND 
            buyer_name = '{}' AND buyer_city = '{}' AND buyer_district = '{}' AND 
            buyer_zip = '{}' AND buyer_address = '{}' AND buyer_phoneNo = '{}' AND
            buyer_cellNo = '{}' AND buyer_email = '{}'
            """.format(user_id, buyer_name, buyer_city, buyer_district, buyer_zip, buyer_address, 
            buyer_phoneNo, buyer_cellNo, buyer_email)
        buyer_result = execSql.execSql(execStr)
        if not buyer_result:
            # 寫進資料庫
            execStr = """INSERT INTO buyer_set(user_id,buyer_name,buyer_city,buyer_district,
                buyer_zip,buyer_address,buyer_phoneNo,buyer_cellNo,buyer_email)
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(user_id,
                buyer_name, buyer_city, buyer_district, buyer_zip, buyer_address, buyer_phoneNo,
                buyer_cellNo, buyer_email)
            execSql.execSql(execStr)
            # 抓剛剛寫進的id
            execStr = """SELECT id FROM buyer_set WHERE user_id = '{}' AND
                buyer_name = '{}' AND buyer_city = '{}' AND buyer_district = '{}' AND
                buyer_zip = '{}' AND buyer_address = '{}' AND buyer_phoneNo = '{}' AND
                buyer_cellNo = '{}' AND buyer_email = '{}'
                """.format(user_id, buyer_name, buyer_city, buyer_district, buyer_zip, buyer_address,
                buyer_phoneNo, buyer_cellNo, buyer_email)
            buyer_result = execSql.execSql(execStr)

        # 拿購物車的資料
        item = json.loads(request.cookies.get('shopCart'))
        datas = []
        detail = ''
        total_amount = 0
        for tmp in item:
            item_id = tmp[0]
            brain = api.content.find(id='%s'%item_id, portal_type='Product')
            for item in brain:
                name = item.Title
                product = item.getObject()
                sale = product.sale_price
                amount = tmp[1]

                detail += '%s x %s x %s,' % (name, amount, sale)
                total_amount += sale * amount

                datas.append({
                    'name': name,
                    'sale': sale,
                    'amount': amount
                })
        buyer_id = dict(buyer_result[0])['id']
        invoice_id = dict(invoice_result[0])['id']
        MerchantTradeNo = int(time.time())
        execStr = """INSERT INTO order_set(MerchantTradeNo, user_id, buyer_id, invoice_id, detail, total_amount) VALUES
            ('{}','{}','{}','{}','{}','{}')""".format(
            MerchantTradeNo, user_id, buyer_id, invoice_id, detail, total_amount)
        execSql.execSql(execStr)

        form_html = '<form id="allPay-Form" name="allPayForm" method="post" target="_self" action="%s/pay" style="display: none;">' %api.portal.get().absolute_url()
        form_html = "".join((form_html, "<input type='hidden' name='{}' value='{}' />".format('MerchantTradeNo', MerchantTradeNo)))
        for data in datas:
            json_data = json.dumps(data)
            form_html = "".join((form_html, "<input type=ahidden' name='{}' value='{}' />".format(data['name'], json_data)))

        form_html = "".join((form_html, '<input type="submit" class="large" id="payment-btn" value="BUY" /></form>'))
        form_html = "".join((form_html, "<script>document.allPayForm.submit();</script>"))
        return form_html


class OrderStatus(BrowserView):
    template = ViewPageTemplateFile("template/order_status.pt")

    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect('%s/login' %api.portal.get().absolute_url())
            api.portal.show_message('%s' % '請先登入'.decode('utf-8'), self.request, 'error')
            return
        try:
            user_id = api.user.get_current().getUserId()
        except:
            if 'Manager' in api.user.get_current().getRoles():
                self.request.response.redirect('%s/all_order_status' %api.portal.get().absolute_url())
                return
        execSql = SqlObj()
        execStr = """SELECT order_set.*,ec_pay.* FROM `order_set`,ec_pay WHERE 
            order_set.user_id = '{}' AND ec_pay.MerchantTradeNo = order_set.MerchantTradeNo
            """.format(user_id)
        result = execSql.execSql(execStr)

        order_data = {}
        for item in result:
            tmp = dict(item)
            MerchantTradeNo = tmp['MerchantTradeNo']
            detail = tmp['detail']
            PaymentType = tmp['PaymentType']
            TradeDate = tmp['TradeDate']
            ExpireDate = tmp['ExpireDate']
            PaymentDate = tmp['PaymentDate']
            total_amount = '%s NT' % tmp['total_amount']
            MerchantID = tmp['MerchantID']

            if tmp['send_time'] == 'morning':
                send_time = '早上'
            elif tmp['send_time'] == 'afternoon':
                send_time = '下午'

            if tmp['send_type'] == 'CVS':
                send_type = '超商取或'
            elif tmp['send_type'] == 'Home':
                send_type = '宅配'

            if tmp['status'] == 'paid':
                status = '以付款'
            elif tmp['status'] == 'not_pay':
                status = '尚未付款'
            # 抓物流訊息
            execStr = """SELECT logistics_set.*,RtnCode_set.message FROM `RtnCode_set`,
                logistics_set WHERE logistics_set.MerchantTradeNo='{}' and logistics_set.RtnCode = 
                RtnCode_set.RtnCode ORDER by UpdateStatusDate DESC""".format(MerchantTradeNo)
            result_RtnCode = execSql.execSql(execStr)

            if result_RtnCode:
                message = dict(result_RtnCode[0])['message']
                UpdateStatusDate = dict(result_RtnCode[0])['UpdateStatusDate']
            else:
                message = False
                UpdateStatusDate = ''

            order_data[MerchantTradeNo] = {
                'MerchantID': MerchantID,
                'detail': detail,
                'total_amount': total_amount,
                'send_time': send_time,
                'send_type': send_type,
                'ExpireDate': ExpireDate,
                'PaymentType': PaymentType,
                'TradeDate': TradeDate,
                'PaymentDate': PaymentDate,
                'message': message,
                'status': status,
                'UpdateStatusDate': UpdateStatusDate
            }
        self.sort_tradeno = sorted(order_data,  reverse=True)
        self.order_data = order_data
        return self.template()



class CoverView(BrowserView):
    template = ViewPageTemplateFile('template/cover.pt')
    def __call__(self):
        return self.template()


class AllOrderStatus(BrowserView):
    template = ViewPageTemplateFile('template/all_order_status.pt')
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect(api.portal.get().absolute_url()/login)
	    return
    	execSql = SqlObj()
        execStr = """SELECT order_set.*,ec_pay.*,invoice_set.*,buyer_set.* FROM `order_set`,ec_pay,invoice_set,buyer_set WHERE 
            ec_pay.MerchantTradeNo = order_set.MerchantTradeNo AND order_set.buyer_id = buyer_set.id 
            AND order_set.invoice_id = invoice_set.id AND ec_pay.flag = 0"""
        result = execSql.execSql(execStr)

        order_data = {}
        for item in result:
            tmp = dict(item)
            MerchantTradeNo = tmp['MerchantTradeNo']
            detail = tmp['detail']
            TradeNo = tmp['TradeNo']
            TradeDate = tmp['TradeDate']
            PaymentDate = tmp['PaymentDate']
            total_amount = '%s NT' % tmp['total_amount']
            MerchantID = tmp['MerchantID']
            status = tmp['status']
            buyer_name = tmp['buyer_name']
            buyer_city = tmp['buyer_city']
            buyer_district = tmp['buyer_district']
            buyer_zip = tmp['buyer_zip']
            buyer_address = tmp['buyer_address']
            buyer_cellNo = tmp['buyer_cellNo']
            buyer_phoneNo = tmp['buyer_phoneNo']
            invoice_code = tmp.get('invoice_code', '')
            invoice_name = tmp['invoice_name']
            # 抓物流訊息
            execStr = """SELECT logistics_set.*,RtnCode_set.message FROM `RtnCode_set`,
                logistics_set WHERE logistics_set.MerchantTradeNo='{}' and logistics_set.RtnCode = 
                RtnCode_set.RtnCode ORDER by UpdateStatusDate DESC""".format(MerchantTradeNo)
            result_RtnCode = execSql.execSql(execStr)

            if result_RtnCode:
                message = dict(result_RtnCode[0])['message']
                UpdateStatusDate = dict(result_RtnCode[0])['UpdateStatusDate']
            else:
                message = False
                UpdateStatusDate = ''

            order_data[MerchantTradeNo] = {
                'MerchantID': MerchantID,
                'TradeNo': TradeNo,
                'detail': detail,
                'total_amount': total_amount,
                'TradeDate': TradeDate,
                'PaymentDate': PaymentDate,
                'message': message,
                'UpdateStatusDate': UpdateStatusDate,
                'status': status,
                'buyer_inform': '%s%s/%s' %(buyer_name,buyer_cellNo, buyer_phoneNo),
                'buyer_name': buyer_name,
                'buyer_cellNo': buyer_cellNo,
                'buyer_phoneNo': buyer_phoneNo,
                'buyer_address': '%s%s%s%s' %(buyer_zip, buyer_city, buyer_district, buyer_address),
                'invoice_name': invoice_name,
                'invoice_code': invoice_code,
            }
        self.sort_tradeno = sorted(order_data,  reverse=True)
        self.order_data = order_data
        return self.template()


class DeleteOrder(BrowserView):
    template = ViewPageTemplateFile('template/all_order_status.pt')
    def __call__(self):
        request = self.request
        MerchantTradeNo = request.get('MerchantTradeNo', '')
        TradeNo = request.get('TradeNo', '')
        if MerchantTradeNo and TradeNo:
            execSql = SqlObj()
            execStr = """UPDATE ec_pay SET flag = 1 WHERE MerchantTradeNo = '{}' AND TradeNo = '{}'""".format(MerchantTradeNo, TradeNo)
            execSql.execSql(execStr)
            request.response.redirect('%s/all_order_status' %(api.portal.get().absolute_url()))
            return

