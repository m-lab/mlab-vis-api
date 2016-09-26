# -*- coding: utf-8 -*-
'''
Endpoints for server asns
'''

from flask_restplus import Resource
from flask import request

from mlab_api.constants import TIME_BINS
# from mlab_api.data.data import SERVER_ASN_DATA as DATA
from mlab_api.data.data import SEARCH_DATA as SEARCH
from mlab_api.rest_api import api
from mlab_api.parsers import search_arguments

from mlab_api.url_utils import get_filter, normalize_key

from mlab_api.models.asn_models import server_asn_search_model

server_asn_ns = api.namespace('servers', description='Server ASN specific API')

@server_asn_ns.route('/search')
class ServerAsnSearch(Resource):
    '''
    Server Search
    '''

    @api.expect(search_arguments)
    @api.marshal_with(server_asn_search_model)
    def get(self):
        """
        Get Server search
        """

        args = search_arguments.parse_args(request)
        search_filter = get_filter(args)
        asn_query = normalize_key(args.get('q'))
        results = SEARCH.get_search_results('servers', asn_query, search_filter)
        return results

# @server_asn_ns.route('/<string:asn_id>/time/<string:time_aggregation>/metrics')
# class ServerAsnTimeMetric(Resource):
#     '''
#     Location Time Metrics
#     '''
#
#     @api.expect(date_arguments)
#     def get(self, asn_id, time_aggregation):
#         """
#         Get Location Metrics Over Time
#         Get speed and other metrics for a particular location at a given time \
#         aggregation level.
#         """
#
#         asn_id = normalize_key(asn_id)
#         args = date_arguments.parse_args(request)
#         (startdate, enddate) = get_time_window(args,
#                                                time_aggregation,
#                                                app.config['DEFAULT_TIME_WINDOWS'])
#
#         results = DATA.get_client_asn_metrics(asn_id, time_aggregation, startdate, enddate)
#         return results
