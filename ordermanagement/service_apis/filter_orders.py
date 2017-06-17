
'''
    @author = Akshay Kale
    date = 2017-06-16 15:34
'''
from flask.globals import request
from ordermanagement.utils.resource import Resource
from ordermanagement.service_api_handlers import get_filtered_orders


class FilterOrders(Resource):

    def get(self):
        '''
        This method retrieves the filtered sale order.
        '''
        data = request.args.to_dict()
        return get_filtered_orders.handle_request(data) 