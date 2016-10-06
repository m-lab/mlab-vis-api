# -*- coding: utf-8 -*-
'''
Utilities to help with formatting the response data
'''
import csv
import cStringIO

from json import dumps
from flask import current_app
from flask_restplus import marshal

def marshal_with_format(format, data, model, to_csv):
    '''
    Marshal data to CSV or to JSON based on a format argument.
    If CSV, then to_csv is called after marshalling with the model.
    '''
    marshaled = marshal(data, model)
    if format == 'csv':
        if to_csv is None:
            print("WARNING: no to_csv provided to marshal with")
            return 'Not supported'
        print("running to_csv but not")
        return 'csv-data'
    print("converting to JSON")
    # otherwise return the JSON as string
    return convert_to_json(marshaled)


def convert_to_csv(rows, fieldnames):
    '''
    Given a list of rows, return them as a CSV string with header row
    '''

    # write to a string
    output = cStringIO.StringIO()
    csvWriter = csv.DictWriter(
        output,
        fieldnames=fieldnames)

    # add the CSV headers
    csvWriter.writeheader()

    # for each row, write it as CSV
    for row in rows:
        csvWriter.writerow(row)

    return output.getvalue()


def convert_to_json(data):
    '''
    Encode the data as JSON -- taken from flask_restplus.representations.output_json
    '''
    settings = current_app.config.get('RESTPLUS_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', True)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(data, **settings) + "\n"

    return dumped
