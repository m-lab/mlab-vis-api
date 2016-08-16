# -*- coding: utf-8 -*-
'''
App Entry Point
'''
from __future__ import print_function

import atexit
import logging

from flask import Flask, request

from flask_restplus import Resource, cors

from mlab_api.data.data import Data
from mlab_api.data.table_config import read_table_configs
from mlab_api.url_utils import get_time_window
from mlab_api.url_utils import format_search_query
from mlab_api.rest_api import api

from mlab_api.parsers import date_arguments
from mlab_api.models import location_search_model, location_metric_model

app = Flask(__name__) #pylint: disable=C0103
app.config.from_object('config')
app.config.SWAGGER_UI_DOC_EXPANSION = 'full'
app.config['RESTPLUS_VALIDATE'] = True

api.decorators = [cors.crossdomain(origin='*')]

locations_ns = api.namespace('locations', description='Location specific API')

TABLE_CONFIGS = read_table_configs(app.config)
DATA = Data(app.config, TABLE_CONFIGS)

@api.route('/connection')
class Connection(Resource):
    '''
    Debug Connection Resource
    '''
    def get(self):
        """
        Lists BigTable Connection Details
        Indicate if a BigTable connection has been made \
        and if so, what tables are accessible to the API.
        ---
        """
        connection = DATA.get_connection()
        if connection:
            return {"message": "Connection", "tables": connection.tables()}
        else:
            return {"message":'No Connection', "tables": []}

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


def exit_handler():
    """
    Called at program exit
    """
    logging.info('Closing Connection')
    DATA.close()

# register exit handler
# TODO: may be a better Flask way to do this.
atexit.register(exit_handler)

# TODO: why in the world does this need to
#  be at the bottom to work ?!?!
api.init_app(app)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
