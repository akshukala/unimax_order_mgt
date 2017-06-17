from uni_db.order_management.models import Order
from django.core.exceptions import ObjectDoesNotExist
from flask import current_app as app

from ordermanagement.core.sale_order_data_handler import SaleOrderDataHandler
from ordermanagement.utils.auth import get_user


def cancel_order(order, reason):
    order.status = reason
    order.modified_by = get_user()
    order.save()
    return {
        "responseCode": 200,
        "Message": "Cancelled"
    }


def edit_order(order, data):
    saleorder = SaleOrderDataHandler(data, csr=order.entered_by, created_on=order.created_on)
    response = saleorder.save()
    if response.get('order_id'):
        order.status = "CANCELLED"
        order.save()
    return response


# def confirm_order(order):
#     order.status = "CREATED"
#     order.modified_by = get_user()
#     order.save()
#     return {
#         'ree' :200,
#         'message' :"Confirmed"
#     }


def handle_request(data):
    '''
    This method handles the  get request,
    Keyword argments
    code -- Sales Order Code
    '''
    try:
        code = data.get("Code")
        order = Order.objects.get(sales_order_id=code)
        if data.get("type", "") == "cancel":
            return cancel_order(order, "CANCELLED")
        elif data.get("type", "") == "edit":
            return edit_order(order, data)
        else:
            return {"responseCode": 200,
                    "Message": "Invalid Request"}

    except ObjectDoesNotExist as o:
        app.logger.info(o)
        return {"responseCode": 200,
                "Message": "Invalid Order Code"}
    except Exception as e:
        app.logger.info(e)
        return {"responseCode": 500,
                "Message": "Internal Server Error"}