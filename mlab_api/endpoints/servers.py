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
from mlab_api.parsers import date_arguments, search_arguments, include_data_arguments, top_arguments

from mlab_api.url_utils import get_time_window, get_filter, normalize_key

from mlab_api.models.location_search_models import location_server_list_model
from mlab_api.models.client_models import client_server_list_model

from mlab_api.models.server_models import server_search_model, server_info_model, server_metric_model
from mlab_api.stats import statsd

server_asn_ns = api.namespace('servers', description='Server ASN specific API')

@server_asn_ns.route('/search')
class ServerSearch(Resource):
    '''
    Server Search
    '''

    @api.expect(search_arguments)
    @api.marshal_with(server_search_model)
    def get(self):
        """
        Search for Servers matching a query.
        """

        args = search_arguments.parse_args(request)
        search_filter = get_filter(args)
        asn_query = normalize_key(args.get('q'))
        results = SEARCH.get_search_results('servers', asn_query, search_filter)
        return results

@server_asn_ns.route('/top')
class ServerTop(Resource):
    '''
    Provide top Servers with provided filters
    '''

    @api.expect(top_arguments)
    @api.marshal_with(server_search_model)
    def get(self):
        """
        Provide top Servers with provided filters
        """

        args = top_arguments.parse_args(request)
        search_filter = get_filter(args)
        results = SEARCH.get_top_results('servers', args.get('limit'), search_filter)
        return results

@server_asn_ns.route('/<string:server_id>')
@server_asn_ns.route('/<string:server_id>/info')
class ServerInfo(Resource):
    '''
    Server Info
    '''
    @api.marshal_with(server_info_model)
    def get(self, server_id):
        """
        Get info for a Server
        """


        results = DATA.get_server_info(server_id)
        return results

@server_asn_ns.route('/<string:server_id>/clients')
class ServerClients(Resource):
    '''
     Server clients List
    '''

    @api.expect(include_data_arguments)
    @api.marshal_with(client_server_list_model)
    @statsd.timer('servers_clients.list.api')
    def get(self, server_id):
        """
        Get list of Clients related to this Server
        """

        args = include_data_arguments.parse_args(request)
        results = DATA.get_server_clients(server_id, args.get('data'))

        return results

@server_asn_ns.route('/<string:server_id>/locations')
class ServerLocations(Resource):
    '''
     Server locations List
    '''

    @api.expect(include_data_arguments)
    @api.marshal_with(location_server_list_model)
    @statsd.timer('servers_locations.list.api')
    def get(self, server_id):
        """
        Get list of Locations related to this Server
        """

        args = include_data_arguments.parse_args(request)
        results = DATA.get_server_locations(server_id, args.get('data'))

        return results

@server_asn_ns.route('/<string:server_id>/metrics')
class ServerTimeMetric(Resource):
    '''
    Location Time Metrics
    '''

    @api.expect(date_arguments)
    @api.marshal_with(server_metric_model)
    @statsd.timer('servers.metrics.api')
    def get(self, server_id):
        """
        Get time-based metrics for a Server
        """

        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_server_metrics(server_id, timebin, startdate, enddate)
        return results
