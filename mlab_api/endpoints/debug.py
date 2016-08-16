# -*- coding: utf-8 -*-
'''
Potentially helpful debugging routes. 
'''
from mlab_api.rest_api import api
from mlab_api.app import DATA

from flask_restplus import Resource


debug_ns = api.namespace('debug', description='Debug Help')

@debug_ns.route('/connection')
class Connection(Resource):
    '''
    Debug Connection Resource
    '''
    def get(self):
        """
        Lists BigTable Connection Details
        Indicate if a BigTable connection has been made \
        and if so, what tables are accessible to the API.
        ---
        """
        connection = DATA.get_connection()
        if connection:
            return {"message": "Connection", "tables": connection.tables()}
        else:
            return {"message":'No Connection', "tables": []}
