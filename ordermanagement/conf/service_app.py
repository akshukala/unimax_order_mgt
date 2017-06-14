'''
    author = Akshay Kale
'''
from os.path import dirname, abspath

import django
from flask import Flask
from flask.ext import restful
from django.db import close_old_connections
from uni_db.settings.pool import init_pool

from flask.ext.cors import CORS
from ordermanagement.session.interfaces import DBInterface
from ordermanagement.conf.config_logger_setup import setup_config_logger
from ordermanagement.service_apis.ping import Ping
# from ordermanagement.service_apis.sale_order import SaleOrder
# from ordermanagement.service_apis.autocomplete import Autocomplete
# from ordermanagement.service_apis.sale_order_edit import EditOrder
# from ordermanagement.service_apis.save_edit_order import Save_Edited_Order
# from ordermanagement.service_apis.coupons import CouponDetails, FarmerCoupons
close_old_connections()
init_pool()

django.setup()


app = Flask(__name__)
CORS(app)
app.auth_header_name = 'X-Authorization-Token'
app.session_interface = DBInterface()
app.root_dir = dirname(dirname(abspath(__file__)))
api = restful.Api(app)
setup_config_logger(app)

app.logger.info("Setting up Resources")

# api.add_resource(SaleOrder, '/ordermanagementservice/saleorder/')
# api.add_resource(Autocomplete, '/ordermanagementservice/autocomplete/')
api.add_resource(Ping, '/ordermanagementservice/ping/')
# api.add_resource(EditOrder, '/ordermanagementservice/editorder/')
# api.add_resource(Save_Edited_Order, '/ordermanagementservice/saveeditorder/')
# api.add_resource(CouponDetails, '/ordermanagementservice/get_coupons/')
# api.add_resource(FarmerCoupons, '/ordermanagementservice/get_farmer_coupon/')

app.logger.info("Resource Setup Done")

if __name__ == '__main__':
#     from gevent import monkey
#     from ordermanagement.utils.hacks import gevent_django_db_hack
#     gevent_django_db_hack()
#     monkey.patch_all()
    app.run(host='0.0.0.0', debug=True, port=7285)
