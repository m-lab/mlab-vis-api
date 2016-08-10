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
