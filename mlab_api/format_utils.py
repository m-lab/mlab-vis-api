# -*- coding: utf-8 -*-
'''
Utilities to help with formatting the response data
'''
import csv
import cStringIO

from json import dumps
from flask import current_app, request

def format_marshaled_data(data, to_csv):
    '''
    Encode data as CSV or to JSON based on a format query string argument or
    if `format` is not available, based on the accepted mediatype.
    If CSV, then to_csv is called to do the formatting.
    '''
    result_format = request.args.get('format')
    if result_format is None:
        # format not in URL, get best guess based on Accept header
        mediatype = request.accept_mimetypes.best_match(
            ['application/json', 'text/csv'],
            default='application/json'
        )
        result_format = 'csv' if mediatype == 'text/csv' else 'json'

    if result_format == 'csv':
        if to_csv is None:
            print "WARNING: no to_csv given to encode with. Encoding as JSON."
        else:
            # convert to CSV via the provided function
            return to_csv(data)

    # otherwise return the JSON as string
    return convert_to_json(data)


def convert_to_csv(rows, fieldnames):
    '''
    Given a list of rows, return them as a CSV string with header row
    '''

    # write to a string
    output = cStringIO.StringIO()
    csv_writer = csv.DictWriter(
        output,
        fieldnames=fieldnames)

    # add the CSV headers
    csv_writer.writeheader()

    # for each row, write it as CSV
    for row in rows:
        csv_writer.writerow(row)

    return output.getvalue()


def cleandict(dictionary):
    '''
    Removes None values from the dictionary. Useful for not having `null` in
    the JSON encoded values. Inspired by http://stackoverflow.com/a/4257279
    '''

    # if a list, clean each item in the list
    if isinstance(dictionary, list):
        return [cleandict(item) for item in dictionary]

    # if not a dictionary or a tuple, just return it
    if not isinstance(dictionary, dict):
        return dictionary

    return dict((key, cleandict(val))
                for key, val in dictionary.iteritems() if val is not None)


def convert_to_json(data):
    '''
    Encode the data as JSON -- taken from
    flask_restplus.representations.output_json -- updated to clean the
    dictionary of nulls.
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
    dumped = dumps(cleandict(data), **settings) + "\n"

    return dumped


def make_data_row(groups):
    '''
    Makes a data row based on groups where a group is so that it can then
    be used to generate a CSV in convert_to_csv.

    `groups` is a list of (dict, fieldnames)

    Example usage:
    make_data_row([(meta, ['client_city', 'client_country']),
        (row, ['count', 'rtt_avg'])])
    '''
    row = {}
    for group in groups:
        (data, fieldnames) = group
        for fieldname in fieldnames:
            if data is not None and fieldname in data:
                row[fieldname] = data[fieldname]
            else:
                row[fieldname] = None

    return row


def meta_results_to_csv(data, meta_fields_dict, data_fields_dict):
    '''
    Helper to create CSV from a set results in { meta: {}, results: [] } format.
    Typically used in metrics results.

    `data`: dictionary of marshaled data
    `meta_fields_dict`: model fields, use .keys() to get fieldnames
    `data_fields_dict`: model fields, use .keys() to get fieldnames
    '''
    meta_fields = meta_fields_dict.keys()
    data_fields = data_fields_dict.keys()

    rows = [make_data_row([(data['meta'] if 'meta' in data else None,
                            meta_fields),
                           (row, data_fields)]) for row in data['results']]
    return convert_to_csv(rows, meta_fields + data_fields)

def meta_in_row_to_csv(data, meta_fields_dict):
    '''
    Helper to create CSV from a set results in { results: [{ meta: {} }] }
    format. Typically used in list results.

    `data`: dictionary of marshaled data
    `meta_fields_dict`: model fields, use .keys() to get fieldnames
    '''
    meta_fields = meta_fields_dict.keys()

    rows = [make_data_row([(row['meta']
                            if 'meta' in row else None, meta_fields)])
            for row in data['results']]
    return convert_to_csv(rows, meta_fields)


def meta_data_in_row_to_csv(data, meta_fields_dict, data_fields_dict):
    '''
    Helper to create CSV from a set results in
    { results: [{ meta: {}, data: {} }] } format. Typically used in search
    results.

    `data`: dictionary of marshaled data
    `meta_fields_dict`: model fields, use .keys() to get fieldnames
    `data_fields_dict`: model fields, use .keys() to get fieldnames
    '''
    meta_fields = meta_fields_dict.keys()
    data_fields = data_fields_dict.keys()

    rows = [make_data_row([(row['meta']
                            if 'meta' in row else None, meta_fields),
                           (row['data']
                            if 'data' in row else None, data_fields)])
            for row in data['results']]
    return convert_to_csv(rows, meta_fields + data_fields)

def meta_data_to_csv(data, meta_fields_dict, data_fields_dict):
    '''
    Helper to create CSV from a set results in { meta: {}, data: {} } format.
    Typically used in info results.

    `data`: dictionary of marshaled data
    `meta_fields_dict`: model fields, use .keys() to get fieldnames
    `data_fields_dict`: model fields, use .keys() to get fieldnames
    '''
    meta_fields = []
    if meta_fields_dict:
        meta_fields = meta_fields_dict.keys()
    data_fields = []
    if data_fields_dict:
        data_fields = data_fields_dict.keys()

    rows = [make_data_row([(data['meta']
                            if 'meta' in data else None, meta_fields),
                           (data['data']
                            if 'data' in data else None, data_fields)])]
    return convert_to_csv(rows, meta_fields + data_fields)
