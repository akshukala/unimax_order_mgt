'''
    @author = Saurabh Gandhi
    date = 2015-10-20 00:10
'''
import json
import traceback
import unittest

from flask import current_app as app

from ordermanagement.conf.config_logger_setup import setup_config_logger


class SaleOrder(unittest.TestCase):
    def __init__(self):
        app.config.update(
            SESSION_COOKIE_DOMAIN=None
        )
        setup_config_logger(app)
        self.client = app.test_client()

    def _process_get_saleOrder(self,code):
        header = {'content-type': 'application/json'}
