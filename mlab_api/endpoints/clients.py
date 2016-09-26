# -*- coding: utf-8 -*-
'''
Endpoints for client asns
'''

from flask_restplus import Resource
from flask import request

from mlab_api.data.data import CLIENT_ASN_DATA as DATA
from mlab_api.data.data import SEARCH_DATA as SEARCH
from mlab_api.constants import TIME_BINS
from mlab_api.rest_api import api
from mlab_api.parsers import date_arguments, search_arguments

from mlab_api.url_utils import get_time_window, get_filter, normalize_key

from mlab_api.models.asn_models import client_asn_search_model

client_asn_ns = api.namespace('clients', description='Client ASN specific API')

@client_asn_ns.route('/search')
class ClientAsnSearch(Resource):
    '''
    Client Search
    '''

    @api.expect(search_arguments)
    @api.marshal_with(client_asn_search_model)
    def get(self):
        """
        Get ASN Metrics Over Time
        """

        args = search_arguments.parse_args(request)
        asn_query = normalize_key(args.get('q'))
        search_filter = get_filter(args)
        results = SEARCH.get_search_results('clients', asn_query, search_filter)
        return results

@client_asn_ns.route('/<string:asn_id>/metrics')
class ClientAsnTimeMetric(Resource):
    '''
    Client Metrics
    '''

    @api.expect(date_arguments)
    def get(self, asn_id):
        """
        Get Client Metrics Over Time
        Get speed and other metrics for a particular client at a given time bin level
        """

        asn_id = normalize_key(asn_id)
        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_client_asn_metrics(asn_id, timebin, startdate, enddate)
        return results
