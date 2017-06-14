'''
    @author = Saurabh Gandhi
    date = 2015-10-15 15:50
'''
from flask_restful import Resource


class Ping(Resource):
    def get(self):
        return {'success': 'True', 'code': 200}
