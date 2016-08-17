'''
Test Data Module
'''
import mlab_api.data.data_utils as du

from tests.utils import read_json


URL_DELIM = "+"

def test_location_key_fields():
    '''
    test get_location_key_fields
    '''

    CONFIG_FILENAME = 'bigtable_configs/client_loc_by_day.json'
    config = read_json(CONFIG_FILENAME)
    assert len(config) > 1


    fields = du.get_location_key_fields(URL_DELIM.join(["NAUSKSKansasCity"]), config)

    assert len(fields) == 1

    # TODO: get this value from config directly instead of hard coded.
    assert len(fields[0]) == 50



def test_decode():
    '''
    test decode
    '''

    value = du.decode_value('this is a string', 'string')
    assert isinstance(value, str)
    assert value == 'this is a string'

    value = du.decode_value('?u\xB7\xD7vZT\xEC', 'double')
    assert isinstance(value, float)
    assert value == 0.005

    value = du.decode_value('12', 'integer')
    assert isinstance(value, int)
    assert value == 12


def test_parse_data():
    '''
    test parse_data
    '''

    config = {'client_city': {'name':'client_city', 'type':'string'}, 'median_download': {'type':'double'}}
    data = {'data:median_download': '@:\xADQ\x83\xBE\x02O', 'meta:client_city': b'New York'}

    result = du.parse_row(data, config)

    assert len(result.keys()) > 1

    assert 'data' in result
    assert 'meta' in result
    assert 'median_download' in result['data']

    assert isinstance(result['data']['median_download'], float)
