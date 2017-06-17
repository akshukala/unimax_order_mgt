#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @author = Akshay Kale
    date = 2017-06-16 15:54
'''


# from DBLayer.Customer.models import Farmer, ShippingAddress, BillingAddress
# from DBLayer.order_management.models import Order, OrderItem, Tag, CallTagMapping
from uni_db.client_erp.models import Client, ShippingAddress, BillingAddress
from uni_db.order_management.models import Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from flask import current_app as app
import requests

from ordermanagement.utils.auth import get_user
from ordermanagement.utils.orderDiscounttoItems import (
    updateOrderDiscountToItems,
    updateAdvancedAmount, hold_neg_disc_order
)
from ordermanagement.utils.utility_functions import get_iso_date


class SaleOrderDataHandler():
    '''
    This class is used to manipulate data on the Sale Order Object.
    '''
    def __init__(self, data, csr=None, created_on=None):
        '''
        Initializes the Class with the data .
        '''
        self.order_data = data
        self.order_items = data['SaleOrderItems']
        self.created_on = created_on
        if csr is None:
            self.csr = get_user()
        else:
            self.csr = csr

    def save_sale_order(self):

        try:
            try:
                owner = Client.objects.get(client_id=self.
                                           order_data['ClientId'])
            except ObjectDoesNotExist:
                return {"responseCode": 422,
                        "Message": "Client with given Id does not exist"}
            shipping_address = ShippingAddress.objects.get(
                id=self.order_data['SAddressId'])
            billing_address = BillingAddress.objects.get(
                id=self.order_data['BAddressId'])
            try:
                order = Order.objects.create(owner=owner,
                                             shipping_address=shipping_address,
                                             billing_address=billing_address)
                if self.created_on:
                    order.created_on = self.created_on
                    order.save()
            except Exception as e:
                app.logger.info(e)
                app.logger.info("Missing Parameters")
                return {"responseCode": 400,
                        "Message": "Bad Request"}

            if 'CashOnDelivery' in self.order_data.keys():
                cod = self.order_data['CashOnDelivery']
                if cod == "false":
                    order.cash_on_delivery = False
                else:
                    order.cash_on_delivery = True
            if 'OrderDiscount' in self.order_data.keys():
                order.order_discount = float(self.order_data['OrderDiscount'])
            if 'TotalDiscount' in self.order_data.keys():
                order.total_discount = float(self.order_data['TotalDiscount'])
            if 'InternalNote' in self.order_data.keys():
                order.internal_note = self.order_data['InternalNote']
            if 'AdvancePayment' in self.order_data.keys():
                order.advance_payment = self.order_data['AdvancePayment']
            if 'AdvPayNote' in self.order_data.keys():
                order.adv_pay_note = self.order_data['AdvPayNote']
            if 'GrandTotal' in self.order_data.keys():
                order.grand_total = float(self.order_data['GrandTotal'])
            if 'CodAmount' in self.order_data.keys():
                order.cod_amount = float(self.order_data['CodAmount'])
            if 'AdvanceOrderDate' in self.order_data.keys():
                order.advance_order_date = get_iso_date(
                    self.order_data['AdvanceOrderDate'])
                if order.advance_order_date:
                    order.status = "FUTURE ORDER"

#             if 'couponCode' in self.order_data.keys():
#                 CouponInfo.objects.get_or_create(coupon=Coupon.objects.get(id=int(self.order_data['couponCode'])),farmer=owner)
            order.entered_by = self.csr
            order.modified_by = get_user()
            order.save()
            app.logger.info("Saved Order for Order %s", order.sales_order_id)
            return order

        except Exception as e:
            app.logger.info(e)
            return {"responseCode": 500,
                    "Message": "Internal Error"}

    def save_sale_order_items(self, order):
        for item in self.order_items:
            try:
                order_item = OrderItem.objects.create(
                    order=order,
                    discount=float(0),
                    list_price=float(item['ListPrice']),
                    selling_price=float(item['SellingPrice']),
                    total_price=float(item['TotalPrice']),
                    quantity=float(item['Quantity'])
                )
                order_item.order = order
                order_item.item_name = item['ItemName']
                order_item.item_sku = item['ItemName']
                order_item.on_hold = True
                order_item.save()
                app.logger.info("Saved Order Items for Order %s",
                                order.sales_order_id)
            except KeyError as e:
                app.logger.info(e)
                return {"responseCode": 400,
                        "Message": "Bad Request"}
            except Exception as e:
                app.logger.info(e)
                return {"responseCode": 500,
                        "Message": "Internal Error"
                        }

    def send_order_created_sms(self, sales_order_id, order_item, cod_amount,
                               caller_id):
        msg = u'आपली ऑर्डर ' + str(order_item)[0:20] + u'... किंमत '  + str(cod_amount)+u' यशस्वीरीत्या घेतली गेली आहे. आपला ऑर्डर नंबर '  + str(sales_order_id) +u' आहे . Krishi Ex मध्ये खरेदी केल्याबद्दल धन्यवाद .'    
        params = {'user': 'krishiex',
                  'password': 'krishiex@123',
                  'sid': 'KRISHI',
                  'msisdn': caller_id,
                  'msg': msg,
                  'fl': 0,
                  'gwid': 2,
                  'dc': 8}
        endpoint = 'http://sms.domainadda.com/vendorsms/pushsms.aspx'
        headers = {'content-type': 'application/json'}
        requests.get(endpoint,
                     params=params,
                     headers=headers)

    def save(self):
        try:
            order = self.save_sale_order()
            order.refresh_from_db()
            app.logger.info("Created order object %s",
                            order.sales_order_id)
            self.save_sale_order_items(order)
            updateOrderDiscountToItems(order)
            updateAdvancedAmount(order)
            hold_neg_disc_order(order)
#             item_name = " ".join([item.item_name.split("-")[1] for item in OrderItem.objects.filter(order=order)])

#             self.send_order_created_sms(str(order.sales_order_id),str(item_name),
#                                         str(order.cod_amount),order.owner.mobile_1)
            return {
                'responseCode': 200,
                'Message': "Order saved",
                'order_id': order.sales_order_id
            }
        except Exception as e:
            app.logger.debug(str(e))
            return {'responseCode': 500,
                    'Message': "Order not saved"}