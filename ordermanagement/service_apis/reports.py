
'''
    @author = Akshay Kale
    date = 2017-06-16 15:34
'''
from flask.globals import request
from ordermanagement.utils.resource import Resource
from ordermanagement.reports import get_order_report_handler


class Reports(Resource):
    def get(self):
        '''
        This method retrieves the filtered sale order.
        '''
        data = request.args.to_dict()
        print data
        return get_order_report_handler.handle_request(data) 
    get.authenticated = False