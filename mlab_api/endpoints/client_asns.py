
from flask_restplus import Resource
from flask import request

from mlab_api.app import app, DATA
from mlab_api.rest_api import api
from mlab_api.parsers import date_arguments

from mlab_api.url_utils import get_time_window, normalize_key

from mlab_api.models.asn_models import client_asn_search_model

client_asn_ns = api.namespace('client_asns', description='Client ASN specific API')

@client_asn_ns.route('/<string:asn_id>/time/<string:time_aggregation>/metrics')
class ClientAsnTimeMetric(Resource):
    '''
    Location Time Metrics
    '''

    @api.expect(date_arguments)
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

@client_asn_ns.route('/search/<string:asn_query>')
class ClientAsnSearch(Resource):
    '''
    Location Time Metrics
    '''

    @api.marshal_with(client_asn_search_model)
    def get(self, asn_query):
        """
        Get Location Metrics Over Time
        Get speed and other metrics for a particular location at a given time \
        aggregation level.
        """

        asn_query = normalize_key(asn_query)
        results = DATA.get_asn_search(asn_query)
        return results
