# -*- coding: utf-8 -*-
'''
App Entry Point
'''
from __future__ import print_function

import traceback
import atexit
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS

from api.data.data import Data
from api.data.table_config import read_table_configs
from api.url_utils import get_time_window
from api.url_utils import format_search_query


app = Flask(__name__) #pylint: disable=C0103
CORS(app)
app.config.from_object('config')

TABLE_CONFIGS = read_table_configs(app.config)
DATA = Data(app.config, TABLE_CONFIGS)




@app.route('/')
def api_root():
    '''
    Placeholder root
    '''
    return jsonify({"message":'Welcome'})

@app.route('/connection')
def api_connection():
    '''
    Indicate if a BigTable connection has been made
    and if so, what tables are accessible to the API.
    '''
    connection = DATA.get_connection()
    if connection:
        return jsonify({"message": "Connection", "tables": connection.tables()})
    else:
        return jsonify({"message":'No Connection', "tables": []})

@app.route('/locations', methods=['GET'])
def get_locations():
    '''
    Return all location ids
    '''

    #locations = DATA.get_locations()
    return jsonify({'locations': ['New York', 'Atlanta']})

@app.route('/locations/search/<location_query>', methods=['GET'])
def get_matching_locations(location_query):
    '''
    Return all location data matching the location_query
    '''

    location_query = format_search_query(location_query)

    try:
        results = DATA.get_location_search(location_query)
        return jsonify({'results': results})
    except Exception as err: #pylint: disable=W0703
        print(str(err))
        traceback.print_exc()
        return jsonify({'error': str(err)})

@app.route('/locations/<location_id>/time/<time_aggregation>/metrics', methods=['GET'])
def get_location(location_id, time_aggregation):
    '''
    Return data for specific location
    '''

    (starttime, endtime) = get_time_window(request.args,
                                           time_aggregation,
                                           app.config['DEFAULT_TIME_WINDOWS'])

    try:
        results = DATA.get_location_metrics(location_id, time_aggregation, starttime, endtime)
        return jsonify(results)
    except Exception as err: #pylint: disable=W0703
        logging.exception(str(err))
        traceback.print_exc()
        return jsonify({'error': str(err)})


@app.route('/locations/<location_id>/time/<time_aggregation>/clientisps/<client_isp_id>/metrics',
           methods=['GET'])
def get_client_isp_in_location(location_id, time_aggregation, client_isp_id):
    '''
    Return data for specific location and specific client ISP
    '''

    (starttime, endtime) = get_time_window(request.args,
                                           time_aggregation,
                                           app.config['DEFAULT_TIME_WINDOWS'])

    try:
        results = DATA.get_location_client_isp_metrics(location_id, client_isp_id,
                                                       time_aggregation, starttime, endtime)

        return jsonify(results)
    except Exception as err: #pylint: disable=W0703
        print(str(err))
        traceback.print_exc()
        return jsonify({'error': str(err)})


@app.errorhandler(500)
def server_error(err):
    '''
    Handle error during request.
    '''
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500

def exit_handler():
    '''
    Called at program exit
    '''
    logging.info('Closing Connection')
    DATA.close()

# register exit handler
# TODO: may be a better Flask way to do this.
atexit.register(exit_handler)

if __name__ == '__main__':
    app.run(port=8080)
