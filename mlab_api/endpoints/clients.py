# -*- coding: utf-8 -*-
# pylint: disable=no-self-use
'''
Endpoints for client asns
'''

from flask_restplus import Resource
from flask import request

from mlab_api.data.data import CLIENT_ASN_DATA as DATA
from mlab_api.data.data import SEARCH_DATA as SEARCH
from mlab_api.constants import TIME_BINS
from mlab_api.rest_api import API
from mlab_api.parsers import DATE_ARGUMENTS, SEARCH_ARGUMENTS, \
    INCLUDE_DATA_ARGUMENTS, TOP_ARGUMENTS

from mlab_api.url_utils import get_time_window, get_filter, normalize_key

from mlab_api.models.location_models import LOCATION_CLIENT_LIST_MODEL, \
    location_client_list_to_csv
from mlab_api.models.client_models import CLIENT_SEARCH_MODEL, \
    client_search_to_csv, CLIENT_INFO_MODEL, client_info_to_csv, \
    CLIENT_METRIC_MODEL, client_metric_to_csv, \
    CLIENT_SERVER_METRIC_MODEL, client_server_metric_to_csv, \
    CLIENT_SERVER_LIST_MODEL, client_server_list_to_csv

from mlab_api.decorators import format_response


CLIENT_ASN_NS = API.namespace('clients', description='Client ASN specific API')

@CLIENT_ASN_NS.route('/search')
class ClientAsnSearch(Resource):
    '''
    Client Search
    '''

    @API.expect(SEARCH_ARGUMENTS)
    @format_response(client_search_to_csv)
    @API.marshal_with(CLIENT_SEARCH_MODEL)
    def get(self):
        """
        Search clients for a given query (ASN Name or ASN Number)
        """

        args = SEARCH_ARGUMENTS.parse_args(request)
        asn_query = normalize_key(args.get('q'))
        search_filter = get_filter(args)
        results_by_name = SEARCH.get_search_results('clients', asn_query, search_filter)
        results_by_number = SEARCH.get_search_results('asn_numbers', asn_query, search_filter)

        merged = results_by_name.copy()
        merged['results'] += results_by_number['results']
        return merged

@CLIENT_ASN_NS.route('/top')
class ClientAsnTop(Resource):
    '''
    Provide Top Clients with given filters
    '''

    @API.expect(TOP_ARGUMENTS)
    @format_response(client_search_to_csv)
    @API.marshal_with(CLIENT_SEARCH_MODEL)
    def get(self):
        """
        Get Client Metrics Over Time
        """

        args = TOP_ARGUMENTS.parse_args(request)
        search_filter = get_filter(args)
        results = SEARCH.get_top_results('clients', args.get('limit'),
                                         search_filter)
        return results

@CLIENT_ASN_NS.route('/<string:client_id>')
@CLIENT_ASN_NS.route('/<string:client_id>/info')
class ClientInfo(Resource):
    '''
    Client Info
    '''
    @format_response(client_info_to_csv)
    @API.marshal_with(CLIENT_INFO_MODEL)
    def get(self, client_id):
        """
        Get info for a Client
        """


        results = DATA.get_client_info(client_id)
        return results

@CLIENT_ASN_NS.route('/<string:client_id>/servers')
class ClientServers(Resource):
    '''
     Client servers List
    '''

    @API.expect(INCLUDE_DATA_ARGUMENTS)
    @format_response(client_server_list_to_csv)
    @API.marshal_with(CLIENT_SERVER_LIST_MODEL)
    def get(self, client_id):
        """
        Get list of Servers related to this Client
        """

        args = INCLUDE_DATA_ARGUMENTS.parse_args(request)
        results = DATA.get_client_servers(client_id, args.get('data'))

        return results

@CLIENT_ASN_NS.route('/<string:client_id>/locations')
class ClientLocations(Resource):
    '''
     Client locations List
    '''

    @API.expect(INCLUDE_DATA_ARGUMENTS)
    @format_response(location_client_list_to_csv)
    @API.marshal_with(LOCATION_CLIENT_LIST_MODEL)
    def get(self, client_id):
        """
        Get list of Locations related to this Client
        """

        args = INCLUDE_DATA_ARGUMENTS.parse_args(request)
        results = DATA.get_client_locations(client_id, args.get('data'))

        return results

@CLIENT_ASN_NS.route('/<string:client_id>/metrics')
class ClientAsnTimeMetric(Resource):
    '''
    Client Metrics
    '''

    @API.expect(DATE_ARGUMENTS)
    @format_response(client_metric_to_csv)
    @API.marshal_with(CLIENT_METRIC_MODEL)
    def get(self, client_id):
        """
        Get time-based metrics for a particular Client.
        """

        args = DATE_ARGUMENTS.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_client_metrics(client_id, timebin, startdate,
                                          enddate)
        return results


@CLIENT_ASN_NS.route('/<string:client_id>/servers/<string:server_id>/metrics')
class ClientServerTimeMetric(Resource):
    '''
    Location + Server Time Metric Resource
    '''

    @API.expect(DATE_ARGUMENTS)
    @format_response(client_server_metric_to_csv)
    @API.marshal_with(CLIENT_SERVER_METRIC_MODEL)
    def get(self, client_id, server_id):
        """
        Get time-based metrics for a specific Client + Server
        """

        args = DATE_ARGUMENTS.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_client_server_metrics(
            client_id, server_id, timebin, startdate, enddate)

        return results
