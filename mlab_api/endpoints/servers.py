# -*- coding: utf-8 -*-
# pylint: disable=no-self-use
'''
Endpoints for server asns
'''

from flask_restplus import Resource
from flask import request

from mlab_api.constants import TIME_BINS
from mlab_api.data.data import SERVER_ASN_DATA as DATA
from mlab_api.data.data import SEARCH_DATA as SEARCH
from mlab_api.rest_api import API
from mlab_api.parsers import DATE_ARGUMENTS, SEARCH_ARGUMENTS, \
    INCLUDE_DATA_ARGUMENTS, TOP_ARGUMENTS

from mlab_api.url_utils import get_time_window, get_filter, normalize_key

from mlab_api.models.location_models import LOCATION_SERVER_LIST_MODEL, \
    location_server_list_to_csv
from mlab_api.models.client_models import CLIENT_SERVER_LIST_MODEL, \
    client_server_list_to_csv

from mlab_api.models.server_models import SERVER_SEARCH_MODEL, \
    server_search_to_csv, SERVER_INFO_MODEL, server_info_to_csv, \
    SERVER_METRIC_MODEL, server_metric_to_csv

from mlab_api.decorators import format_response
from mlab_api.stats import ANALYTICS

SERVER_ASN_NS = API.namespace('servers', description='Server ASN specific API')

@SERVER_ASN_NS.route('/search')
class ServerSearch(Resource):
    '''
    Server Search
    '''

    @API.expect(SEARCH_ARGUMENTS)
    @format_response(server_search_to_csv)
    @API.marshal_with(SERVER_SEARCH_MODEL)
    def get(self):
        """
        Search for Servers matching a query.
        """

        args = SEARCH_ARGUMENTS.parse_args(request)
        search_filter = get_filter(args)
        asn_query = normalize_key(args.get('q'))
        results = SEARCH.get_search_results('servers', asn_query, search_filter)
        return results

@SERVER_ASN_NS.route('/top')
class ServerTop(Resource):
    '''
    Provide top Servers with provided filters
    '''

    @API.expect(TOP_ARGUMENTS)
    @format_response(server_search_to_csv)
    @API.marshal_with(SERVER_SEARCH_MODEL)
    def get(self):
        """
        Provide top Servers with provided filters
        """

        args = TOP_ARGUMENTS.parse_args(request)
        search_filter = get_filter(args)
        results = SEARCH.get_top_results('servers', args.get('limit'),
                                         search_filter)
        return results

@SERVER_ASN_NS.route('/<string:server_id>')
@SERVER_ASN_NS.route('/<string:server_id>/info')
class ServerInfo(Resource):
    '''
    Server Info
    '''
    @format_response(server_info_to_csv)
    @API.marshal_with(SERVER_INFO_MODEL)
    def get(self, server_id):
        """
        Get info for a Server
        """


        results = DATA.get_server_info(server_id)
        return results

@SERVER_ASN_NS.route('/<string:server_id>/clients')
class ServerClients(Resource):
    '''
     Server clients List
    '''

    @API.expect(INCLUDE_DATA_ARGUMENTS)
    @format_response(client_server_list_to_csv)
    @API.marshal_with(CLIENT_SERVER_LIST_MODEL)
    @ANALYTICS.timer('api_call', 'servers_clients.list.api')
    def get(self, server_id):
        """
        Get list of Clients related to this Server
        """

        args = INCLUDE_DATA_ARGUMENTS.parse_args(request)
        results = DATA.get_server_clients(server_id, args.get('data'))

        return results

@SERVER_ASN_NS.route('/<string:server_id>/locations')
class ServerLocations(Resource):
    '''
     Server locations List
    '''

    @API.expect(INCLUDE_DATA_ARGUMENTS)
    @format_response(location_server_list_to_csv)
    @API.marshal_with(LOCATION_SERVER_LIST_MODEL)
    @ANALYTICS.timer('api_call', 'servers_locations.list.api')
    def get(self, server_id):
        """
        Get list of Locations related to this Server
        """

        args = INCLUDE_DATA_ARGUMENTS.parse_args(request)
        results = DATA.get_server_locations(server_id, args.get('data'))

        return results

@SERVER_ASN_NS.route('/<string:server_id>/metrics')
class ServerTimeMetric(Resource):
    '''
    Location Time Metrics
    '''

    @API.expect(DATE_ARGUMENTS)
    @format_response(server_metric_to_csv)
    @API.marshal_with(SERVER_METRIC_MODEL)
    @ANALYTICS.timer('api_call', 'servers.metrics.api')
    def get(self, server_id):
        """
        Get time-based metrics for a Server
        """

        args = DATE_ARGUMENTS.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_server_metrics(server_id, timebin, startdate,
                                          enddate)
        return results
