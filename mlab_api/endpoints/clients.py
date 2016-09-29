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
from mlab_api.parsers import date_arguments, search_arguments, include_data_arguments

from mlab_api.url_utils import get_time_window, get_filter, normalize_key

from mlab_api.models.asn_models import client_asn_search_model, client_asn_info_model, client_metric_model

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

@client_asn_ns.route('/<string:client_id>')
@client_asn_ns.route('/<string:client_id>/info')
class ClientInfo(Resource):
    '''
    Client Info
    '''
    @api.marshal_with(client_asn_info_model)
    def get(self, client_id):
        """
        Cliet Info
        Get info for a particular client.
        """


        results = DATA.get_client_info(client_id)
        return results

@client_asn_ns.route('/<string:client_id>/servers')
class ClientServers(Resource):
    '''
     Client  servers List
    '''

    @api.expect(include_data_arguments)
    def get(self, client_id):
        """
        Get list of servers related to this client
        """

        args = include_data_arguments.parse_args(request)
        results = DATA.get_client_servers(client_id, args.get('data'))

        return results

@client_asn_ns.route('/<string:client_id>/locations')
class ClientLocations(Resource):
    '''
     Client  locations List
    '''

    @api.expect(include_data_arguments)
    def get(self, client_id):
        """
        Get list of clients related to this server
        """

        args = include_data_arguments.parse_args(request)
        results = DATA.get_client_locations(client_id, args.get('data'))

        return results

@client_asn_ns.route('/<string:client_id>/metrics')
class ClientAsnTimeMetric(Resource):
    '''
    Client Metrics
    '''

    @api.expect(date_arguments)
    @api.marshal_with(client_metric_model)
    def get(self, client_id):
        """
        Get Client Metrics Over Time
        Get speed and other metrics for a particular client at a given time bin level
        """

        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_client_metrics(client_id, timebin, startdate, enddate)
        return results


@client_asn_ns.route('/<string:client_id>/servers/<string:server_id>/metrics')
class ClientServerTimeMetric(Resource):
    '''
    Location + Server Time Metric Resource
    '''

    @api.expect(date_arguments)
    def get(self, client_id, server_id):
        """
        Get time metrics for a specific client + server
        """

        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_client_server_metrics(client_id, server_id,
                                                   timebin, startdate, enddate)

        return results
