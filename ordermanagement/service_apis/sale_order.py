
'''
    @author = Akshay Kale
    date = 2017-06-16 15:34
'''

from flask import current_app as app
from flask.globals import request
from ordermanagement.utils.resource import Resource
from ordermanagement.service_api_handlers import (
    get_sale_order_handler,
    put_sale_order_handler,
    post_sale_order_handler
)


class SaleOrder(Resource):
    '''
    This API creates new Sale Order and retrieves the older Sale Order Details.
    '''

    def get(self):
        '''
        This method retrieves the old sale order. Taking the Sale Order Code 
        as parameter.
        '''
        app.logger.info(request)
        data = request.args
        code = data['Code']
        app.logger.info("Received GET Sale Order request for Code %s",
                        code)
        return get_sale_order_handler.handle_request(code)

    def put(self):
        '''
        This method retrieves the old sale order. Taking the Sale Order Code 
        as parameter.
        '''
        app.logger.info(request)
        data = request.get_json(force=True)
        app.logger.info("Received PUT Sale Order request for Code %s",
                        data)
        return put_sale_order_handler.handle_request(data)

    def post(self):
        '''
        This method creates new Sale Order.
        '''
        app.logger.info(request)
        request_details = request.get_json(force=True)
        print request_details
        app.logger.info("Received POST Sale Order request for Code %s",
                        request_details)
        return post_sale_order_handler.handle_request(request_details)