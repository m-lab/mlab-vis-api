# -*- coding: utf-8 -*-
'''
General purpose decorators
'''

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
