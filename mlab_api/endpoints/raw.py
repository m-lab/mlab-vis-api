# -*- coding: utf-8 -*-
'''
Sample Raw Data
'''
from mlab_api.rest_api import api
from mlab_api.data.data import RAW_DATA as DATA

from flask_restplus import Resource


raw_ns = api.namespace('raw', description='')

@raw_ns.route('/tests')
class RawTests(Resource):
    '''

    '''
    def get(self):
        """
        Returns a sample of raw upload/download data including lat/lon positions.
        """
        results = DATA.get_raw_test_results()
        return results
