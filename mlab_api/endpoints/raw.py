# -*- coding: utf-8 -*-
# pylint: disable=no-self-use
'''
Sample Raw Data
'''
from mlab_api.rest_api import API
from mlab_api.data.data import RAW_DATA as DATA

from flask_restplus import Resource


RAW_NS = API.namespace('raw', description='')

@RAW_NS.route('/tests')
class RawTests(Resource):
    '''
    Raw data tests
    '''
    def get(self):
        """
        Returns a sample of raw upload/download data including lat/lon
        positions.
        """
        results = DATA.get_raw_test_results()
        return results
