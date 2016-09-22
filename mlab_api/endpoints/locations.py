# -*- coding: utf-8 -*-
'''
Routes focused on locations.
'''

from flask import request
from flask_restplus import Resource

from mlab_api.app import app
from mlab_api.data.data import LOCATION_DATA as DATA
from mlab_api.data.data import SEARCH_DATA as SEARCH
from mlab_api.parsers import date_arguments, type_arguments, include_data_arguments, search_arguments
from mlab_api.models.location_search_models import location_search_model
from mlab_api.models.location_metric_models import location_metric_model
from mlab_api.models.location_info_models import location_info_model, location_children_model, location_client_isp_info_model

from mlab_api.url_utils import get_time_window, normalize_key, get_filter

from mlab_api.rest_api import api

from mlab_api.stats import statsd

# this is the namespace that gets included elsewhere.
locations_ns = api.namespace('locations', description='Location specific API')

@locations_ns.route('/<string:location_id>')
@locations_ns.route('/<string:location_id>/info')
class LocationInfo(Resource):
    '''
    Location Info
    '''
    # @api.marshal_with(location_search_model)
    @statsd.timer('locations.info.api')
    def get(self, location_id):
        """
        Location Info
        Get all location data matching the location_query
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
    @api.marshal_with(location_children_model)
    @statsd.timer('locations.children.api')
    def get(self, location_id):
        """
        Location Search
        Get all location data matching the location_query
        """

        args = type_arguments.parse_args(request)
        location_id = normalize_key(location_id)

        results = DATA.get_location_children(location_id, args.get('type'))
        return results

@locations_ns.route('/search/<string:location_query>')
class LocationSearch(Resource):
    '''
    Location Search Resource
    '''
    @api.expect(search_arguments)
    @api.marshal_with(location_search_model)
    @statsd.timer('locations.search.api')
    def get(self, location_query):
        """
        Location Search
        Get all location data matching the location_query
        """

        location_query = normalize_key(location_query)
        args = search_arguments.parse_args(request)
        search_filter = get_filter(args)
        results = SEARCH.get_search_results('locations', location_query, search_filter)

        return results

@locations_ns.route('/<string:location_id>/time/<string:time_aggregation>/metrics')
class LocationTimeMetric(Resource):
    '''
    Location Time Metrics
    '''

    @api.expect(date_arguments)
    @api.marshal_with(location_metric_model)
    @statsd.timer('locations.metrics.api')
    def get(self, location_id, time_aggregation):
        """
        Get Location Metrics Over Time
        Get speed and other metrics for a particular location at a given time \
        aggregation level.
        """

        location_id = normalize_key(location_id)
        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args,
                                               time_aggregation,
                                               app.config['DEFAULT_TIME_WINDOWS'])

        results = DATA.get_location_metrics(location_id, time_aggregation, startdate, enddate)
        return results

@locations_ns.route('/<string:location_id>/time/<string:time_aggregation>/clients/<string:client_isp_id>/metrics')
class LocationTimeClientIspMetric(Resource):
    '''
    Location Time ISP Resource
    '''

    @api.expect(date_arguments)
    @statsd.timer('locations.clientisps_metrics.api')
    def get(self, location_id, time_aggregation, client_isp_id):
        """
        Get Location Metrics for ISP Over Time
        Get metrics for specific location and specific client ISP
        """

        location_id = normalize_key(location_id)

        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args,
                                               time_aggregation,
                                               app.config['DEFAULT_TIME_WINDOWS'])

        results = DATA.get_location_client_isp_metrics(location_id, client_isp_id,
                                                       time_aggregation, startdate, enddate)

        return results

@locations_ns.route('/<string:location_id>/clients')
class LocationClientIspStats(Resource):
    '''
    Location ISP Resource
    '''

    @api.expect(include_data_arguments)
    @statsd.timer('locations.clientisps_list.api')
    def get(self, location_id):
        """
        Get Location Metrics for ISP Over Time
        Get metrics for specific location and specific client ISP
        """

        location_id = normalize_key(location_id)

        args = include_data_arguments.parse_args(request)


        results = DATA.get_location_client_isps(location_id, args.get('data'))

        return results

@locations_ns.route('/<string:location_id>/clients/<string:client_isp_id>/info')
class LocationClientIspInfo(Resource):
    '''
    Location ISP Resource info
    '''

    @api.marshal_with(location_client_isp_info_model)
    @statsd.timer('locations.clientisps_info.api')
    def get(self, location_id, client_isp_id):
        """
        Get ISP info for a specific location / isp combo
        """

        location_id = normalize_key(location_id)


        results = DATA.get_location_client_isp_info(location_id, client_isp_id)


        return results
