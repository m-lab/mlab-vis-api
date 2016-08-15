'''
App Entry Point
'''
from __future__ import print_function

import traceback
import atexit
import logging

from flask import Flask, request, jsonify
from flask_restplus import Resource, Api
from flask_cors import CORS


from api.data.data import Data
from api.data.table_config import read_table_configs
from api.url_utils import get_time_window
from api.url_utils import format_search_query

from api.parsers import date_arguments


app = Flask(__name__) #pylint: disable=C0103
CORS(app)
app.config.from_object('config')

api = Api(app)
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
        tags:
        - debug
        """
        connection = DATA.get_connection()
        if connection:
            return jsonify({"message": "Connection", "tables": connection.tables()})
        else:
            return jsonify({"message":'No Connection', "tables": []})

@locations_ns.route('/<string:location_id>/time/<string:time_aggregation>/metrics')
class LocationTimeMetric(Resource):
    '''
    Location Time Resource
    '''

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

        try:
            results = DATA.get_location_metrics(location_id, time_aggregation, startdate, enddate)
            return jsonify(results)
        except Exception as err: #pylint: disable=W0703
            logging.exception(str(err))
            traceback.print_exc()
            return jsonify({'error': str(err)})

@locations_ns.route('/<string:location_id>/time/<string:time_aggregation>/clientisps/<string:client_isp_id>/metrics')
class LocationTimeIspMetric(Resource):
    '''
    Location Time ISP Resource
    '''
    def get(self, location_id, time_aggregation, client_isp_id):
        """
        Get Location Metrics for ISP Over Time
        Get metrics for specific location and specific client ISP
        """

        args = date_arguments.parse_args(request)
        (startdate, enddate) = get_time_window(args,
                                               time_aggregation,
                                               app.config['DEFAULT_TIME_WINDOWS'])

        try:
            results = DATA.get_location_client_isp_metrics(location_id, client_isp_id,
                                                           time_aggregation, startdate, enddate)

            return jsonify(results)
        except Exception as err: #pylint: disable=W0703
            print(str(err))
            traceback.print_exc()
            return jsonify({'error': str(err)})

@locations_ns.route('/search/<string:location_query>')
class LocationSearch(Resource):
    '''
    Location Search Resource
    '''
    def get(self, location_query):
        """
        Location Search
        Get all location data matching the location_query
        """

        location_query = format_search_query(location_query)

        try:
            results = DATA.get_location_search(location_query)
            return jsonify({'results': results})
        except Exception as err: #pylint: disable=W0703
            print(str(err))
            traceback.print_exc()
            return jsonify({'error': str(err)})


@app.errorhandler(500)
def server_error(err):
    """
    Handle error during request.
    """
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500

def exit_handler():
    """
    Called at program exit
    """
    logging.info('Closing Connection')
    DATA.close()

# register exit handler
# TODO: may be a better Flask way to do this.
atexit.register(exit_handler)

if __name__ == '__main__':
    app.run(port=8080)
