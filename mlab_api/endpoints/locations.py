# -*- coding: utf-8 -*-
'''
Routes focused on locations.
'''

from flask import request
from flask_restplus import Resource

from mlab_api.app import app, DATA
from mlab_api.parsers import date_arguments
from mlab_api.models.location_search_models import location_search_model
from mlab_api.models.location_metric_models import location_metric_model

from mlab_api.url_utils import get_time_window, normalize_key

from mlab_api.rest_api import api

# this is the namespace that gets included elsewhere.
locations_ns = api.namespace('locations', description='Location specific API')


@locations_ns.route('/<string:location_id>/time/<string:time_aggregation>/metrics')
class LocationTimeMetric(Resource):
    '''
    Location Time Metrics
    '''

    @api.expect(date_arguments)
    @api.marshal_with(location_metric_model)
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

@locations_ns.route('/<string:location_id>/time/<string:time_aggregation>/clientisps/<string:client_isp_id>/metrics')
class LocationTimeClientIspMetric(Resource):
    '''
    Location Time ISP Resource
    '''

    @api.expect(date_arguments)
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

@locations_ns.route('/search/<string:location_query>')
class LocationSearch(Resource):
    '''
    Location Search Resource
    '''
    @api.marshal_with(location_search_model)
    def get(self, location_query):
        """
        Location Search
        Get all location data matching the location_query
        """

        location_query = normalize_key(location_query)

        results = DATA.get_location_search(location_query)
        return results

@locations_ns.route('/<string:location_id>/children')
class LocationChildren(Resource):
    '''
    Location Children List
    '''
    # @api.marshal_with(location_search_model)
    def get(self, location_id):
        """
        Location Search
        Get all location data matching the location_query
        """

        location_id = normalize_key(location_id)

        results = DATA.get_location_children(location_id)
        return results
