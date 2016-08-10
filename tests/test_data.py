'''
Test Data Module
'''
from api.data.data import Data

from tests.utils import read_json

CONFIG_FILENAME = 'tests/mocks/bigtable_config.json'

def test_key_creation():
    config = read_json(CONFIG_FILENAME)
    assert(len(config) > 1)

    d = Data({}, [])

    fields = d.get_location_key_fields("NA+US+KS+Kansas City", config)

    assert(len(fields) == 4)
    # city has 40 length
    # TODO: get this value from config directly instead of hard coded.
    assert(len(fields[-1]) == 40)


def test_get_location_type():
    d = Data({}, [])
    country_type = d.get_location_type('NA+US')
    assert(country_type == 'client_country')

    country_type = d.get_location_type('NA+US+KS')
    assert(country_type == 'client_region')

    country_type = d.get_location_type('NA+US+KS+Kansas City')
    assert(country_type == 'client_city')
