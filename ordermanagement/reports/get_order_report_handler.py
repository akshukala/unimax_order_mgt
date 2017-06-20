'''
    @author = Ganesh Bodkhe
'''
from uni_db.order_management.models import (
    Order, OrderItem
)
import os
import xlwt
from datetime import datetime
from os.path import dirname
from flask_restful import Resource
from flask import current_app as app
from flask.helpers import send_from_directory


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
            os.makedirs(dir)


def create_excel(path, data):
    # import pdb
    # pdb.set_trace()
    print data.get('to_date')
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("Unimax")
    style_header_title = xlwt.easyxf('alignment: horiz centre; font: bold on, height 230, name Arial; borders: left thin, top thin, bottom thin, right thin')
    style_header_info = xlwt.easyxf('alignment: horiz left; font: bold on, height 200, name Arial; borders: left thin, top thin, bottom thin, right thin')
    style_header_body_title = xlwt.easyxf('align: horiz centre, wrap on; font: bold on, height 200, name Arial; borders: left thin, top thin, bottom thin, right thin')
    style_header_body_text = xlwt.easyxf('align: horiz centre, wrap on; font: height 200, name Arial; borders: left thin, top thin, bottom thin, right thin')

    sheet1.write(4, 0, "Order Id.", style_header_body_title)
    sheet1.write(4, 1, "Order Id.", style_header_body_title)
    sheet1.write(4, 2, "Client Name", style_header_body_title)
    sheet1.write(4, 3, "client Id", style_header_body_title)
    sheet1.write(4, 4, "Cost", style_header_body_title)
    sheet1.write(4, 5, "Created Date", style_header_body_title)
    sheet1.write(4, 6, "Created By", style_header_body_title)
    sheet1.write(4, 7, "Status", style_header_body_title)
    sheet1.write(4, 8, "Items Name", style_header_body_title)

    excel_counter = 5
    order_obj = Order.objects.filter(created_on__range=[data.get('from_date'),
                                      data.get('to_date')]).exclude(status='CANCELLED')
    for i,order in enumerate(order_obj):
        sheet1.write(excel_counter, 0, str(i+1), style_header_body_text)
        sheet1.write(excel_counter, 1, str(order.sales_order_id), style_header_body_text)
        sheet1.write(excel_counter, 2, str(order.owner.client_name), style_header_body_text)
        sheet1.write(excel_counter, 3, str(order.owner.client_id), style_header_body_text)
        sheet1.write(excel_counter, 4, str(order.grand_total), style_header_body_text)
        sheet1.write(excel_counter, 5, order.created_on.strftime("%d/%m/%Y"), style_header_body_text)
        sheet1.write(excel_counter, 6, str(order.entered_by.username), style_header_body_text)
        sheet1.write(excel_counter, 7, str(order.status), style_header_body_text)
        orderitem_list = []
        item_name = ""
        for orderitem in OrderItem.objects.filter(order=order):
            split_item_name = str(orderitem.item_name).split('-')
            item_name += split_item_name[1]+", "
            # orderitem_list.append(split_item_name[1])
        sheet1.write(excel_counter, 8, str(item_name), style_header_body_text)
        excel_counter = excel_counter + 1
    sheet1.write(excel_counter, 9, '', style_header_body_title)
    book.save(path)

def handle_request(data):
    UPLOAD_FOLDER = os.path.join(dirname(app.root_dir), 'documents')
    print UPLOAD_FOLDER
    filename = str(datetime.today().strftime("%d_%m_%y")) + "unimax.xls" 
    path = os.path.join(UPLOAD_FOLDER, filename)
    assure_path_exists(path)
    create_excel(path, data)
    return send_from_directory(directory=UPLOAD_FOLDER, filename=filename)
