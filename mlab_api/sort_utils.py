# -*- coding: utf-8 -*-
'''
Utilities to sort
'''


def sort_by_count(row):
    '''
    Given a row, return its test_count or last_year_test_count,
    if present
    '''
    if 'test_count' in row['meta']:
        return row['meta']['test_count']
    elif 'last_year_test_count' in row['meta']:
        return row['meta']['last_year_test_count']
    else:
        return 'a'
