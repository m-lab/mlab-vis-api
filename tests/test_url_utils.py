# -*- coding: utf-8 -*-
'''
Test URL Utils
'''

from mlab_api.url_utils import normalize_key, get_filter


def test_normalize_key():
    '''
    Test normalizing a key
    '''

    inkey = ' a b cde '
    outkey = normalize_key(inkey)

    assert outkey == 'abcde'

    inkey = 'AT&T & Friends'
    outkey = normalize_key(inkey)

    assert outkey == 'attfriends'

    inkey = 'saco34bogotá'
    outkey = normalize_key(inkey)
    assert outkey == 'saco34bogotá'


def test_get_filter():
    '''
    Test getting a filter out of a type and value
    '''

    params = {'filtertype': 'locations', 'filtervalue': 'nausny'}

    filter_dict = get_filter(params)

    assert 'value' in filter_dict
    assert filter_dict['value'][0] == 'nausny'
