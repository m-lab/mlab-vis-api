'''
Test Decorators
'''

from mlab_api.decorators import add_id

@add_id('id_name')
def simple_add_id():
    return {'meta':{'id_name': 'aaa'}}

@add_id(['id1', 'id2'])
def compound_add_id(have_meta=True):
    if have_meta:
        return {'meta':{'id1':'aaa', 'id2':'bbb'}}
    else:
        return {'id1':'aaa', 'id2':'bbb'}


def test_simple_add_id():
    results = simple_add_id()
    assert(results['meta']['id'] == 'aaa')

def test_compound_add_id():
    results = compound_add_id()
    assert(results['meta']['id'] == 'aaa_bbb')

def test_no_meta_add_id():
    results = compound_add_id(have_meta=False)
    assert(results['id1'] == 'aaa')
