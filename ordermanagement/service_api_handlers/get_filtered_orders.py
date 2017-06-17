'''
    @author = Akshay Kale
'''
from uni_db.order_management.models import (
    Order, OrderItem
)


def filter_by_area(area):
    response = []
    for order in Order.objects.filter(shipping_address__area=area
                                      ).exclude(status='CANCELLED'):
        order_dict = {}
        order_dict['order_id'] = str(order.sales_order_id)
        order_dict['clientname'] = str(order.owner.client_name)
        order_dict['client_id'] = str(order.owner.client_id)
        order_dict['cost'] = order.grand_total
        order_dict['created_date'] = order.created_on.strftime("%d/%m/%Y")
        order_dict['created_by'] = order.entered_by.username
        order_dict['status'] = str(order.status)
        orderitem_list = []
        for orderitem in OrderItem.objects.filter(order=order):
            split_item_name = str(orderitem.item_name).split('-')
            orderitem_list.append(split_item_name[1])
        order_dict['item_names'] = orderitem_list
        response.append(order_dict)
    return response


def handle_request(data):
    if str(data.get('type')) == 'area':
        return filter_by_area(str(data.get('text_data')))
