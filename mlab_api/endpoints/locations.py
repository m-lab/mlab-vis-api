# -*- coding: utf-8 -*-

from flask import request
from flask_restplus import Resource

from mlab_api.app import app, DATA
from mlab_api.parsers import date_arguments
from mlab_api.models.location_search_models import location_search_model
from mlab_api.models.location_metric_models import location_metric_model

from mlab_api.url_utils import get_time_window
from mlab_api.url_utils import format_search_query

from mlab_api.rest_api import api
locations_ns = api.namespace('locations', description='Location specific API')


@locations_ns.route('/<string:location_id>/time/<string:time_aggregation>/metrics')
class LocationTimeMetric(Resource):
    '''
    Location Time Resource
    '''

    @api.expect(date_arguments)
    @api.marshal_with(location_metric_model)
    def get(self, location_id, time_aggregation):
        """
        Get Location Metrics Over Time
        Get speed and other metrics for a particular location at a given time \
        aggregation level.
        """

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

        location_query = format_search_query(location_query)

        results = DATA.get_location_search(location_query)
        return results
