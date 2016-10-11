# -*- coding: utf-8 -*-
'''
Setup API instance.
'''
import logging

from flask_restplus import Api
from flask import make_response

# This is connected to the app in
# main.py
api = Api(version='0.1.0', doc='/', title='MLab API', default_mediatype='text/plain')

@api.errorhandler
def server_error(err):
    """
    Handle error during request.
    """
    logging.exception('An error occurred during a request.')
    logging.exception(err)
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(err), 500


@api.representation('text/csv')
def csv_mediatype_representation(data, code, headers):
    """
    Assume the data is already marshaled to CSV and just write it
    to the response
    """
    return raw_response(data, code, headers)


@api.representation('application/json')
def json_mediatype_representation(data, code, headers):
    """
    Assume the data is already marshaled to JSON and just write it
    to the response
    """
    return raw_response(data, code, headers)

def raw_response(data, code, headers):
    """
    Assume the data is already marshaled and just writes it to the response.
    """
    if not isinstance(data, basestring):
        print('Expected string data, but received:')
        print(data)
        data = '"Error: Malformed response"'

    resp = make_response(data, code)
    resp.headers.extend(headers)
    print(resp.headers, headers)

    return resp
