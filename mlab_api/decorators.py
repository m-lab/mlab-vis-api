# -*- coding: utf-8 -*-
'''
General purpose decorators
'''

def add_id(id_attribute):
    def add_id_decorator(func):
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
    return add_id_decorator
