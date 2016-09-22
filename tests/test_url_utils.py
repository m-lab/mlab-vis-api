'''
Test URL Utils
'''

from mlab_api.url_utils import normalize_key


def test_normalize_key():

    inkey = ' a b cde '
    outkey = normalize_key(inkey)

    assert(outkey == 'abcde')

    inkey = 'AT&T & Friends'
    outkey = normalize_key(inkey)

    assert(outkey == 'attfriends')
