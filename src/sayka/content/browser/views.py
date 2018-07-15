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
        receiver_name = request.get('receiver_name', '')
        receiver_city = request.get('receiver_city', '')
        receiver_district = request.get('receiver_district', '')
        receiver_zip = request.get('receiver_zip', '')
        receiver_address = request.get('receiver_address', '')
        receiver_phoneNo = request.get('receiver_phoneNo', '')
        receiver_cellNo = request.get('receiver_cellNo', '')
        receiver_email = request.get('receiver_email', '')
        send_time = request.get('send_time', '')
        send_type = request.get('send_type', '')
        invoice_district = request.get('invoice_district', '')
        invoice_zip = request.get('invoice_zip', '')
        invoice_city = request.get('invoice_city', '')
        invoice_code = request.get('invoice_code', '')
        invoice_name = request.get('invoice_name', '')
        invoice_address = request.get('invoice_address', '')
        invoice_type = request.get('invoice_type', '')

        user_id = api.user.get_current().getUserId()
        user_name = api.user.get_current().getUserName()
        user = api.user.get(user_name)

        # if user_name == buyer_name:
        #     user.setMemberProperties(mapping={
        #                                         'city': buyer_city,
        #                                         'district': buyer_district,
        #                                         'zip': buyer_zip,
        #                                         'cellNo': buyer_cellNo,
        #                                         'phoneNo': buyer_phoneNo,
        #                                         'email': buyer_email,
        #                                         'address': buyer_address
        #                                     })

        # 寫進發票的常用資料庫
        add_invoice = request.get('add_invoice', '')
        execStr = """SELECT id FROM invoice_set WHERE user_id = '{}' AND invoice_name = '{}' 
            AND invoice_city = '{}' AND invoice_district = '{}' AND invoice_zip = '{}' 
            AND invoice_address = '{}' AND invoice_code = '{}' AND invoice_type = '{}' 
            AND address_book = '{}'""".format(user_id, invoice_name, 
            invoice_city,invoice_district, invoice_zip, invoice_address, invoice_code,
            invoice_type, add_invoice)
        invoice_result = execSql.execSql(execStr)
        if not invoice_result:
            # 寫進資料庫及判斷要不要加進常用通訊錄
            execStr = """INSERT INTO invoice_set(user_id,invoice_name,invoice_city,invoice_district,
                invoice_zip,invoice_address,invoice_code,invoice_type,address_book) 
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(user_id, 
                invoice_name, invoice_city, invoice_district, invoice_zip, invoice_address, 
                invoice_code, invoice_type, add_invoice)
            execSql.execSql(execStr)
            # 抓剛剛寫進的id
            execStr = """SELECT id FROM invoice_set WHERE user_id = '{}' AND 
                invoice_name = '{}' AND invoice_city = '{}' AND invoice_district = '{}' AND 
                invoice_zip = '{}'  AND invoice_address = '{}' AND invoice_code = '{}' 
                AND invoice_type = '{}' AND address_book = '{}'
                """.format(user_id, invoice_name, invoice_city, invoice_district, invoice_zip, 
                invoice_address, invoice_code, invoice_type, add_invoice)
            invoice_result = execSql.execSql(execStr)

        # 訂購人寫進資料庫
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

        # 收件人寫進資料庫
        add_receiver = request.get('add_receiver', '')
        execStr = """SELECT id FROM receiver_set WHERE user_id = '{}' AND receiver_name = '{}' 
            AND receiver_city = '{}' AND receiver_district = '{}' AND receiver_zip = '{}' 
            AND receiver_address = '{}' AND receiver_phoneNo = '{}' AND receiver_cellNo = '{}' 
            AND receiver_email = '{}' AND address_book = '{}'""".format(user_id, receiver_name, 
            receiver_city, receiver_district, receiver_zip, receiver_address, receiver_phoneNo, 
            receiver_cellNo, receiver_email, add_receiver)
        receiver_result = execSql.execSql(execStr)
        if not receiver_result:
            # 寫進資料庫及判斷要不要加進常用通訊錄
            execStr = """INSERT INTO receiver_set(user_id,receiver_name,receiver_city,receiver_district,
                receiver_zip,receiver_address,receiver_phoneNo,receiver_cellNo,receiver_email,address_book) 
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(user_id, 
                receiver_name, receiver_city, receiver_district, receiver_zip, receiver_address, receiver_phoneNo,
                receiver_cellNo, receiver_email, add_receiver)
            execSql.execSql(execStr)
            # 抓剛剛寫進的id
            execStr = """SELECT id FROM receiver_set WHERE user_id = '{}' AND 
                receiver_name = '{}' AND receiver_city = '{}' AND receiver_district = '{}' AND 
                receiver_zip = '{}' AND receiver_address = '{}' AND receiver_phoneNo = '{}' AND
                receiver_cellNo = '{}' AND receiver_email = '{}' AND address_book = '{}'
                """.format(user_id, receiver_name, receiver_city, receiver_district, receiver_zip, receiver_address, 
                receiver_phoneNo, receiver_cellNo, receiver_email, add_receiver)
            receiver_result = execSql.execSql(execStr)

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
        receiver_id = dict(receiver_result[0])['id']
        invoice_id = dict(invoice_result[0])['id']
        MerchantTradeNo = int(time.time())
        execStr = """INSERT INTO order_set(MerchantTradeNo,user_id,buyer_id,receiver_id,invoice_id,detail,
            total_amount,send_time,send_type) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(
            MerchantTradeNo, user_id, buyer_id, receiver_id, invoice_id, detail, total_amount
            , send_time, send_type)
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
        execStr = """SELECT order_set.*,ec_pay.* FROM `order_set`,ec_pay WHERE 
            ec_pay.MerchantTradeNo = order_set.MerchantTradeNo"""
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

