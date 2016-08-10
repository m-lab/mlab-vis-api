'''
Test Data Module
'''
import api.data.data_utils as du

from tests.utils import read_json


URL_DELIM = "+"

def test_location_key_fields():
    '''
    test get_location_key_fields
    '''

    CONFIG_FILENAME = 'bigtable_configs/client_city_by_day.json'
    config = read_json(CONFIG_FILENAME)
    assert len(config) > 1


    fields = du.get_location_key_fields(URL_DELIM.join(["NA", "US", "KS", "Kansas City"]), config)

    assert len(fields) == 4

    # city has 40 length
    # TODO: get this value from config directly instead of hard coded.
    assert len(fields[-1]) == 40


def test_get_location_type():
    '''
    Test get_location_type
    '''
    country_type = du.get_location_type(URL_DELIM.join(["NA", "US"]))
    assert country_type == 'client_country'

    country_type = du.get_location_type(URL_DELIM.join(["NA", "US", "KS"]))
    assert country_type == 'client_region'

    country_type = du.get_location_type(URL_DELIM.join(["NA", "US", "KS", "Kansas City"]))
    assert country_type == 'client_city'

    country_type = du.get_location_type(URL_DELIM.join(["NA", "US", "KS", "KS", "KS","KS"]))
    assert country_type == 'unknown'


def test_decode():
    '''
    test decode
    '''

    value = du.decode('this is a string', 'string')
    assert isinstance(value, str)
    assert value == 'this is a string'

    value = du.decode('?u\xB7\xD7vZT\xEC', 'double')
    assert isinstance(value, float)
    assert value == 0.005

    value = du.decode('12', 'integer')
    assert isinstance(value, int)
    assert value == 12


def test_parse_data():
    '''
    test parse_data
    '''

    config = {'client_city': {'name':'client_city', 'type':'string'}, 'median_download': {'type':'double'}}
    data = {'data:median_download': '@:\xADQ\x83\xBE\x02O', 'meta:client_city': b'New York'}

    result = du.parse_data(data, config)

    assert len(result.keys()) > 1

    assert 'data' in result
    assert 'meta' in result
    assert 'median_download' in result['data']

    assert isinstance(result['data']['median_download'], float)
