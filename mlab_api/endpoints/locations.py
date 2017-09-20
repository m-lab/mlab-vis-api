# -*- coding: utf-8 -*-
# pylint: disable=no-self-use
'''
Routes focused on locations.
'''

from flask import request
from flask_restplus import Resource

from mlab_api.constants import TIME_BINS
from mlab_api.data.data import LOCATION_DATA as DATA
from mlab_api.data.data import SEARCH_DATA as SEARCH
from mlab_api.parsers import DATE_ARGUMENTS, TYPE_ARGUMENTS, \
    INCLUDE_DATA_ARGUMENTS, SEARCH_ARGUMENTS, TOP_ARGUMENTS

from mlab_api.models.location_models import LOCATION_SEARCH_MODEL, \
    location_search_to_csv, LOCATION_CLIENT_LIST_MODEL, \
    location_client_list_to_csv, LOCATION_SERVER_LIST_MODEL, \
    location_server_list_to_csv, LOCATION_METRIC_MODEL, \
    location_metric_to_csv, LOCATION_CLIENT_METRIC_MODEL, \
    location_client_metric_to_csv, LOCATION_SERVER_METRIC_MODEL, \
    location_server_metric_to_csv, LOCATION_CLIENT_SERVER_METRIC_MODEL, \
    location_client_server_metric_to_csv, LOCATION_INFO_MODEL, \
    location_info_to_csv, LOCATION_CHILDREN_MODEL, location_children_to_csv, \
    LOCATION_CLIENT_ISP_INFO_MODEL, location_client_isp_info_to_csv


from mlab_api.url_utils import get_time_window, normalize_key, get_filter
from mlab_api.decorators import format_response

from mlab_api.rest_api import API
from mlab_api.stats import ANALYTICS

# this is the namespace that gets included elsewhere.
LOCATIONS_NS = API.namespace('locations', description='Location specific API')

@LOCATIONS_NS.route('/search')
class LocationSearch(Resource):
    '''
    Location Search Resource
    '''
    @API.expect(SEARCH_ARGUMENTS)
    @format_response(location_search_to_csv)
    @API.marshal_with(LOCATION_SEARCH_MODEL)
    def get(self):
        """
        Get all Locations matching a query
        """

        args = SEARCH_ARGUMENTS.parse_args(request)
        location_query = normalize_key(args.get('q'))
        search_filter = get_filter(args)
        results = SEARCH.get_search_results('locations', location_query,
                                            search_filter)

        return results

@LOCATIONS_NS.route('/top')
class LocationTop(Resource):
    '''
    Provide top Locations with provided filters
    '''

    @API.expect(TOP_ARGUMENTS)
    @format_response(location_search_to_csv)
    @API.marshal_with(LOCATION_SEARCH_MODEL)
    def get(self):
        """
        Get top locations with given filters
        """

        args = TOP_ARGUMENTS.parse_args(request)
        search_filter = get_filter(args)
        results = SEARCH.get_top_results('locations', args.get('limit'),
                                         search_filter)
        return results

@LOCATIONS_NS.route('/<string:location_id>')
@LOCATIONS_NS.route('/<string:location_id>/info')
class LocationInfo(Resource):
    '''
    Location Info
    '''
    @format_response(location_info_to_csv)
    @API.marshal_with(LOCATION_INFO_MODEL)
    @ANALYTICS.timer('api_call', 'locations.info.api')
    def get(self, location_id):
        """
        Get information for a Location
        """

        location_id = normalize_key(location_id)

        results = DATA.get_location_info(location_id)
        return results


@LOCATIONS_NS.route('/<string:location_id>/children')
class LocationChildren(Resource):
    '''
    Location Children List
    '''
    @API.expect(TYPE_ARGUMENTS)
    @format_response(location_children_to_csv)
    @API.marshal_with(LOCATION_CHILDREN_MODEL)
    @ANALYTICS.timer('api_call', 'locations.children.api')
    def get(self, location_id):
        """
        Get Locations matching a query
        """

        args = TYPE_ARGUMENTS.parse_args(request)
        location_id = normalize_key(location_id)

        results = DATA.get_location_children(location_id, args.get('type'))
        return results

@LOCATIONS_NS.route('/<string:location_id>/clients')
class LocationClients(Resource):
    '''
    Location Clients Resource
    '''

    @API.expect(INCLUDE_DATA_ARGUMENTS)
    @format_response(location_client_list_to_csv)
    @API.marshal_with(LOCATION_CLIENT_LIST_MODEL)
    @ANALYTICS.timer('api_call', 'locations_clients.list.api')
    def get(self, location_id):
        """
        Get list of Clients related to this Location
        """

        location_id = normalize_key(location_id)

        args = INCLUDE_DATA_ARGUMENTS.parse_args(request)
        results = DATA.get_location_clients(location_id, args.get('data'))

        return results

@LOCATIONS_NS.route('/<string:location_id>/servers')
class LocationServers(Resource):
    '''
     Location + Server List
    '''

    @API.expect(INCLUDE_DATA_ARGUMENTS)
    @format_response(location_server_list_to_csv)
    @API.marshal_with(LOCATION_SERVER_LIST_MODEL)
    @ANALYTICS.timer('api_call', 'locations_servers.list.api')
    def get(self, location_id):
        """
        Get list of Servers related to this Location
        """

        location_id = normalize_key(location_id)

        args = INCLUDE_DATA_ARGUMENTS.parse_args(request)
        results = DATA.get_location_servers(location_id, args.get('data'))

        return results


@LOCATIONS_NS.route('/<string:location_id>/clients/<string:client_isp_id>/info')
class LocationClientIspInfo(Resource):
    '''
    Location ISP Resource info
    '''

    @format_response(location_client_isp_info_to_csv)
    @API.marshal_with(LOCATION_CLIENT_ISP_INFO_MODEL)
    @ANALYTICS.timer('api_call', 'locations.clientisps_info.api')
    def get(self, location_id, client_isp_id):
        """
        Get info for a particular Location + Client
        """

        location_id = normalize_key(location_id)


        results = DATA.get_location_client_isp_info(location_id, client_isp_id)


        return results

@LOCATIONS_NS.route('/<string:location_id>/metrics')
class LocationTimeMetric(Resource):
    '''
    Location Time Metrics
    '''

    @API.expect(DATE_ARGUMENTS)
    @format_response(location_metric_to_csv)
    @API.marshal_with(LOCATION_METRIC_MODEL)
    @ANALYTICS.timer('api_call', 'locations.metrics.api')
    def get(self, location_id):
        """
        Get time-based metrics for a Location
        """

        location_id = normalize_key(location_id)
        args = DATE_ARGUMENTS.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_location_metrics(location_id, timebin, startdate,
                                            enddate)

        return results

@LOCATIONS_NS.route('/<string:location_id>/clients/<string:client_id>/metrics')
class LocationClientTimeMetric(Resource):
    '''
    Location + Client Time Resource
    '''

    @API.expect(DATE_ARGUMENTS)
    @format_response(location_client_metric_to_csv)
    @API.marshal_with(LOCATION_CLIENT_METRIC_MODEL)
    @ANALYTICS.timer('api_call', 'locations_clients.metrics.api')
    def get(self, location_id, client_id):
        """
        Get time-based metrics for a Location + Client
        """
        location_id = normalize_key(location_id)

        args = DATE_ARGUMENTS.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_location_client_metrics(location_id, client_id,
                                                   timebin, startdate, enddate)

        return results

@LOCATIONS_NS.route('/<string:location_id>/servers/<string:server_id>/metrics')
class LocationServerTimeMetric(Resource):
    '''
    Location + Server Time Metric Resource
    '''

    @API.expect(DATE_ARGUMENTS)
    @format_response(location_server_metric_to_csv)
    @API.marshal_with(LOCATION_SERVER_METRIC_MODEL)
    @ANALYTICS.timer('api_call', 'locations_servers.metrics.api')
    def get(self, location_id, server_id):
        """
        Get time-based metrics for a Location + Server
        """

        location_id = normalize_key(location_id)

        args = DATE_ARGUMENTS.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_location_server_metrics(location_id, server_id,
                                                   timebin, startdate, enddate)

        return results

@LOCATIONS_NS.route('/<string:location_id>/clients/<string:client_id>'+
                    '/servers/<string:server_id>/metrics')
class LocationClientServerTimeMetric(Resource):
    '''
    Location + Client + Server Time Resource
    '''

    @API.expect(DATE_ARGUMENTS)
    @format_response(location_client_server_metric_to_csv)
    @API.marshal_with(LOCATION_CLIENT_SERVER_METRIC_MODEL)
    @ANALYTICS.timer('api_call', 'locations_servers.metrics.api')
    def get(self, location_id, client_id, server_id):
        """
        Get time-based metrics for a Location + Client + Server
        """

        location_id = normalize_key(location_id)

        args = DATE_ARGUMENTS.parse_args(request)
        (startdate, enddate) = get_time_window(args, TIME_BINS)

        timebin = args.get('timebin')
        results = DATA.get_location_client_server_metrics(
            location_id, client_id, server_id, timebin, startdate, enddate)

        return results
