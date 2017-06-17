'''
    @author = Akshay Kale
'''
import json

from uni_db.order_management.models import (
    Order, OrderItem, OrderStatusHistory
)
from uni_db.client_erp.models import ClientMobile
#from DBLayer.inventory.models import Delivery
from django.core.exceptions import ObjectDoesNotExist
from ordermanagement.utils.address_utils import address_as_json
from flask import current_app as app
from ordermanagement.utils.auth import get_user
from ordermanagement.utils.JsonSerializer import JSONSerializer
from ordermanagement.utils.utility_functions import (
    get_str_datetime, get_str_date
)


def create_response(order_instance):
    '''
     This method returns the JSON response for the Order.
     Keyword arguments
     order_instance -- Order object
    '''

    serializer = JSONSerializer()
    response = {}
    billing_address = address_as_json(order_instance.billing_address)
    shipping_address = address_as_json(order_instance.shipping_address)
    serialized_sale_order = serializer.serialize(order_instance)
    seriaized_sale_order_item = serializer.serialize([
        json.loads(serializer.serialize(ob)) for ob in
        OrderItem.objects.filter(order=order_instance)
    ])

    serialized_sale_order_history = serializer.serialize([
        json.loads(serializer.serialize(oh)) for oh in
        OrderStatusHistory.objects.filter(order=order_instance)
    ])

#     if(order_instance.status=='DISPATCHED' or order_instance.status=='ORDER COMPLETED' or order_instance.status=='RETURN COMPLETED'):
#         try:
#             response['IndiaPostBarcode']=str(Delivery.objects.get(order=order_instance).indiaPost_barcode_no)
#         except ObjectDoesNotExist:
#             response['IndiaPostBarcode']="Delivery Object Not Created."    
#     else:
#         response['IndiaPostBarcode']='Yet To Dispatch'    
    response['SaleOrder'] = json.loads(serialized_sale_order)
    if order_instance.advance_order_date:
        response['SaleOrder']['advance_order_date'] = get_str_date(
            order_instance.advance_order_date)

    response['SaleOrder']['created_on'] = get_str_datetime(
        order_instance.created_on)
    response['SaleOrder']['updated_on'] = get_str_datetime(
        order_instance.updated_on)

    if order_instance.entered_by:
        response['SaleOrder']['entered_by_csr'] = order_instance.entered_by.get_full_name()
    if order_instance.modified_by:
        response['SaleOrder']['modified_by_csr'] = order_instance.modified_by.get_full_name()

    response['SaleOrder']['billing_address'] = billing_address
    response['SaleOrder']['shipping_address'] = shipping_address
    response['SaleOrder']['notification_mobile'] = [str(mob.mobile) for mob
                                                    in ClientMobile.objects.filter(client=order_instance.owner)]
    response['SaleOrder']['owner'] = {
        'Name': order_instance.owner.client_name,
        'ClientId': order_instance.owner.client_id
    }

    #response['SaleOrder']['coupon_name'] = order_instance.coupon.name if order_instance.coupon else 'None'
    response['SaleOrderItem'] = json.loads(seriaized_sale_order_item)
    response['SaleOrderHistory'] = json.loads(serialized_sale_order_history)
    return response


def handle_request(code):
    '''
    This method handles the  get request,
    Keyword argments
    code -- Sales Order Code
    '''
    try:
        order = Order.objects.get(sales_order_id=code)
        return create_response(order)

    except ObjectDoesNotExist as o:
        app.logger.info(o)
        return {
            "responseCode": 200,
            "Message": "Invalid Order Code"
        }

    except Exception as e:
        app.logger.info(e)
        return {
            "responseCode": 500,
            "Message": "Internal Server Error"
        }