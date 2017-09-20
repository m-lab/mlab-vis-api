# -*- coding: utf-8 -*-
'''
API input parameter parsers.
'''
from flask_restplus import reqparse
from mlab_api.constants import FILTER_TYPES, TIME_BINS

# ---
# Date arguments
# ---
# date arguments allow for start and end dates
# defaults are provided in config
DATE_ARGUMENTS = reqparse.RequestParser()
DATE_ARGUMENTS.add_argument('startdate', type=str, required=False,
                            help='Start date of metrics')
DATE_ARGUMENTS.add_argument('enddate', type=str, required=False,
                            help='End date of metrics')
DATE_ARGUMENTS.add_argument('timebin', type=str, required=False, default='day',
                            choices=TIME_BINS.keys(),
                            help='Time binning to use for time metrics')

# ---
# type arguments
# ---
TYPE_ARGUMENTS = reqparse.RequestParser()
TYPE_ARGUMENTS.add_argument('type', type=str, required=False,
                            choices=['country', 'region', 'city'],
                            help='Limit results to a specific type')


# ---
# include data arguments
# ---
INCLUDE_DATA_ARGUMENTS = reqparse.RequestParser()
INCLUDE_DATA_ARGUMENTS.add_argument('data', type=bool, required=False,
                                    default=False,
                                    help='Include data attributes in results')


# ---
# search arguments
# ---
SEARCH_ARGUMENTS = reqparse.RequestParser()
SEARCH_ARGUMENTS.add_argument('q', required=True,
                              help='Query String')
SEARCH_ARGUMENTS.add_argument('filtertype', type=str, required=False,
                              choices=FILTER_TYPES,
                              help='Filter type works in conjunction with ' +
                              'filtervalue to specify search filter')

SEARCH_ARGUMENTS.add_argument('filtervalue', required=False,
                              help='Limit search to only results with ' +
                              'associations with ids in filtervalue. Id type' +
                              ' is specified in filtertype.')

# ---
# top arguments
# ---
TOP_ARGUMENTS = reqparse.RequestParser()
TOP_ARGUMENTS.add_argument('limit', type=int, required=False, default=20,
                           help='Limits results count to top number')

TOP_ARGUMENTS.add_argument('filtertype', required=True,
                           choices=FILTER_TYPES,
                           help='Filter type works in conjunction with ' +
                           'filtervalue to specify search filter')

TOP_ARGUMENTS.add_argument('filtervalue', required=True,
                           help='Limit search to only results with ' +
                           'associations with ids in filtervalue. Id type ' +
                           'is specified in filtertype.')
