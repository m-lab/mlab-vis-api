# -*- coding: utf-8 -*-
'''
Routes focused on locations.
'''

from flask import request
from flask_restplus import Resource

from mlab_api.constants import TIME_BINS
from mlab_api.data.data import LOCATION_DATA as DATA
from mlab_api.data.data import SEARCH_DATA as SEARCH
from mlab_api.parsers import date_arguments, type_arguments, include_data_arguments, search_arguments, top_arguments

from mlab_api.models.location_models import location_search_model, location_search_to_csv, \
    location_client_list_model, location_client_list_to_csv, \
    location_server_list_model, location_server_list_to_csv, \
    location_metric_model, location_metric_to_csv, \
    location_client_metric_model, location_client_metric_to_csv, \
    location_server_metric_model, location_server_metric_to_csv, \
    location_client_server_metric_model, location_client_server_metric_to_csv, \
    location_info_model, location_info_to_csv, \
    location_children_model, location_children_to_csv, \
    location_client_isp_info_model, location_client_isp_info_to_csv


from mlab_api.url_utils import get_time_window, normalize_key, get_filter
from mlab_api.decorators import format_response

from mlab_api.rest_api import api

from mlab_api.stats import analytics

# this is the namespace that gets included elsewhere.
locations_ns = api.namespace('locations', description='Location specific API')

@locations_ns.route('/search')
class LocationSearch(Resource):
    '''
    Location Search Resource
    '''
    @api.expect(search_arguments)
    @format_response(location_search_to_csv)
    @api.marshal_with(location_search_model)
    def get(self):
        """
        Get all Locations matching a query
        """

        args = search_arguments.parse_args(request)
        location_query = normalize_key(args.get('q'))
        search_filter = get_filter(args)
        results = SEARCH.get_search_results('locations', location_query, search_filter)

        return results

@locations_ns.route('/top')
class LocationTop(Resource):
    '''
    Provide top Locations with provided filters
    '''

    @api.expect(top_arguments)
    @format_response(location_search_to_csv)
    @api.marshal_with(location_search_model)
    def get(self):
        """
        Get top locations with given filters
        """

        args = top_arguments.parse_args(request)
        search_filter = get_filter(args)
        results = SEARCH.get_top_results('locations', args.get('limit'), search_filter)
        return results

@locations_ns.route('/<string:location_id>')
@locations_ns.route('/<string:location_id>/info')
class LocationInfo(Resource):
    '''
    Location Info
    '''
    @format_response(location_info_to_csv)
    @api.marshal_with(location_info_model)
    @analytics.timer('api_call', 'locations.info.api')
    def get(self, location_id):
        """
        Get information for a Location
        """

        location_id = normalize_key(location_id)

        results = DATA.get_location_info(location_id)
        return results


@locations_ns.route('/<string:location_id>/children')
class LocationChildren(Resource):
    '''
    Location Children List
    '''
    @api.expect(type_arguments)
    @format_response(location_children_to_csv)
    @api.marshal_with(location_children_model)
    @analytics.timer('api_call', 'locations.children.api')
    def get(self, location_id):
        """
        Get Locations matching a query
        """

        args = type_arguments.parse_args(request)
        location_id = normalize_key(location_id)

        results = DATA.get_location_children(location_id, args.get('type'))
        return results

@locations_ns.route('/<string:location_id>/clients')
class LocationClients(Resource):
    '''
    Location Clients Resource
    '''

    @api.expect(include_data_arguments)
    @format_response(location_client_list_to_csv)
    @api.marshal_with(location_client_list_model)
    @analytics.timer('api_call', 'locations_clients.list.api')
    def get(self, location_id):
        """
        Get list of Clients related to this Location
        """

        location_id = normalize_key(location_id)

        args = include_data_arguments.parse_args(request)
        results = DATA.get_location_clients(location_id, args.get('data'))

        return results

@locations_ns.route('/<string:location_id>/servers')
class LocationServers(Resource):
    '''
     Location + Server List
    '''

    @api.expect(include_data_arguments)
    @format_response(location_server_list_to_csv)
    @api.marshal_with(location_server_list_model)
    @analytics.timer('api_call', 'locations_servers.list.api')
    def get(self, location_id):
        """
        Get list of Servers related to this Location
        """

        location_id = normalize_key(location_id)

        args = include_data_arguments.parse_args(request)
        results = DATA.get_location_servers(location_id, args.get('data'))

        return results


@locations_ns.route('/<string:location_id>/clients/<string:client_isp_id>/info')
class LocationClientIspInfo(Resource):
    '''
    Location ISP Resource info
    '''

    @format_response(location_client_isp_info_to_csv)
    @api.marshal_with(location_client_isp_info_model)
    @analytics.timer('api_call', 'locations.clientisps_info.api')
    def get(self, location_id, client_isp_id):
        """
        Get info for a particular Location + Client
        """

        location_id = normalize_key(location_id)


        results = DATA.get_location_client_isp_info(location_id, client_isp_id)


        return results

@locations_ns.route('/<string:location_id>/metrics')
class LocationTimeMetric(Resource):
    '''
    Location Time Metrics
    '''

    @api.expect(date_arguments)
    @format_response(location_metric_to_csv)
    @api.marshal_with(location_metric_model)
    @analytics.timer('api_call', 'locations.metrics.api')
    def get(self, location_id):
        """
        Get time-based metrics for a Location
        """

        location_id = normalize_key(location_id)
        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_location_metrics(location_id, timebin, startdate, enddate)

        return results

@locations_ns.route('/<string:location_id>/clients/<string:client_id>/metrics')
class LocationClientTimeMetric(Resource):
    '''
    Location + Client Time Resource
    '''

    @api.expect(date_arguments)
    @format_response(location_client_metric_to_csv)
    @api.marshal_with(location_client_metric_model)
    @analytics.timer('api_call', 'locations_clients.metrics.api')
    def get(self, location_id, client_id):
        """
        Get time-based metrics for a Location + Client
        """

        location_id = normalize_key(location_id)

        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_location_client_metrics(location_id, client_id,
                                                   timebin, startdate, enddate)

        return results

@locations_ns.route('/<string:location_id>/servers/<string:server_id>/metrics')
class LocationServerTimeMetric(Resource):
    '''
    Location + Server Time Metric Resource
    '''

    @api.expect(date_arguments)
    @format_response(location_server_metric_to_csv)
    @api.marshal_with(location_server_metric_model)
    @analytics.timer('api_call', 'locations_servers.metrics.api')
    def get(self, location_id, server_id):
        """
        Get time-based metrics for a Location + Server
        """

        location_id = normalize_key(location_id)

        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_location_server_metrics(location_id, server_id,
                                                   timebin, startdate, enddate)

        return results

@locations_ns.route('/<string:location_id>/clients/<string:client_id>/servers/<string:server_id>/metrics')
class LocationClientServerTimeMetric(Resource):
    '''
    Location + Client + Server Time Resource
    '''

    @api.expect(date_arguments)
    @format_response(location_client_server_metric_to_csv)
    @api.marshal_with(location_client_server_metric_model)
    @analytics.timer('api_call', 'locations_servers.metrics.api')
    def get(self, location_id, client_id, server_id):
        """
        Get time-based metrics for a Location + Client + Server
        """

        location_id = normalize_key(location_id)

        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_location_client_server_metrics(location_id, client_id, server_id,
                                                          timebin, startdate, enddate)

        return results
