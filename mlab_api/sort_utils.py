# -*- coding: utf-8 -*-
'''
Utilities to sort
'''


def sort_by_count(row):
    if 'test_count' in row['meta']:
        return row['meta']['test_count']
    elif 'last_year_test_count' in row['meta']:
        return row['meta']['last_year_test_count']
    else:
        return 'a'
