# -*- coding: utf-8 -*-
'''
General purpose decorators
'''

from functools import update_wrapper
from flask import make_response, request
from mlab_api.format_utils import format_marshaled_data

def add_ids(id_attribute):
    '''
    Decorator that adds an 'id' attribute to each value of the
    returned array. Function it is used on is expected to return
    and array of results with a 'meta' value in each result.
    '''
    def add_ids_decorator(func):
        def func_wrapper(*args, **kwargs):
            results = func(*args, **kwargs)
            if not 'results' in results:
                return results
            for result in results['results']:
                if 'meta' in result:
                    if id_attribute in result['meta']:
                        result['meta']['id'] = result['meta'][id_attribute]

            return results
        return func_wrapper
    return add_ids_decorator

def add_id(id_attribute):
    '''
    Decorator that adds an 'id' attribute to a single value
    Function is expected to return a dict with a 'meta' value
    '''
    if isinstance(id_attribute, basestring):
        id_attribute = [id_attribute]
    def add_id_decorator(func):
        def func_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if 'meta' in result:
                id_values = [result['meta'][attr] for attr in id_attribute if attr in result['meta']]
                result['meta']['id'] = "_".join(id_values)

            return result
        return func_wrapper
    return add_id_decorator

def add_id_value():
    def add_id_decorator(func):
        def func_wrapper(self, id_value, **kwargs):
            result = func(self, id_value, **kwargs)
            if 'meta' in result:
                result['meta']['id'] = id_value

            return result
        return func_wrapper
    return add_id_decorator

def format_from_url_decorator(func):
    '''
    Decorator to handle setting the Content-Type header based on the
    format query parameter if available.
    '''

    def func_wrapper(*args, **kwargs):
        resp = make_response(func(*args, **kwargs))

        # restplus ignores our setting of Content-Type in our mediatype handlers
        # so set it here based on the format parameter
        result_format = request.args.get('format')
        if result_format == 'csv':
            resp.headers['Content-Type'] = 'text/csv'
        elif result_format == 'json':
            resp.headers['Content-Type'] = 'application/json'

        return resp
    return update_wrapper(func_wrapper, func)


def format_response(to_csv=None):
    '''
    Format the marshaled data as CSV or JSON depending on format
    request parameter and Accepts header
    '''
    def format_decorator(func):
        def func_wrapper(*args, **kwargs):
            results = func(*args, **kwargs)
            return format_marshaled_data(results, to_csv)
        return func_wrapper
    return format_decorator


def download_decorator(func):
    def func_wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)

        # ignore if download query param is not set
        if request.args.get('download') is None:
            return resp

        # replace the slashes in the API url to get the filename
        path = request.path if request.path[0] != '/' else request.path[1:]
        filename = path.replace('/', '_')

        # Add in query param values to the filename
        for k, v in request.args.iteritems():
            print('got kv', k, v)
            if k not in ['download', 'format']:
                filename += '_%s' % v

        # add the file extension based on the mimetype
        filetype = 'csv' if resp.headers['Content-Type'] == 'text/csv' else 'json'

        # set the content disposition header so it downloads
        resp.headers['Content-Disposition'] = 'attachment; filename=%s.%s' % (filename, filetype)
        return resp
    return update_wrapper(func_wrapper, func)
