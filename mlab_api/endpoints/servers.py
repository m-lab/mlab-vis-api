# -*- coding: utf-8 -*-
'''
Endpoints for server asns
'''

from flask_restplus import Resource
from flask import request

from mlab_api.constants import TIME_BINS
from mlab_api.data.data import SERVER_ASN_DATA as DATA
from mlab_api.data.data import SEARCH_DATA as SEARCH
from mlab_api.rest_api import api
from mlab_api.parsers import date_arguments, search_arguments

from mlab_api.url_utils import get_time_window, get_filter, normalize_key

from mlab_api.models.asn_models import server_asn_search_model, server_asn_info_model
from mlab_api.stats import statsd

server_asn_ns = api.namespace('servers', description='Server ASN specific API')

@server_asn_ns.route('/search')
class ServerSearch(Resource):
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

@server_asn_ns.route('/<string:server_id>')
@server_asn_ns.route('/<string:server_id>/info')
class ServerInfo(Resource):
    '''
    Server Info
    '''
    @api.marshal_with(server_asn_info_model)
    def get(self, server_id):
        """
        Server Info
        Get info for a particular server.
        """


        results = DATA.get_server_info(server_id)
        return results


@server_asn_ns.route('/<string:server_id>/metrics')
class ServerTimeMetric(Resource):
    '''
    Location Time Metrics
    '''

    @api.expect(date_arguments)
    # @api.marshal_with(location_metric_model)
    @statsd.timer('servers.metrics.api')
    def get(self, server_id):
        """
        Get Server Metrics Over Time
        Get speed and other metrics for a particular server id at a given time \
        aggregation level.
        """

        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_server_metrics(server_id, timebin, startdate, enddate)
        return results
