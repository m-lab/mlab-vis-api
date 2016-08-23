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

    config_filename = 'bigtable_configs/client_loc_by_day.json'
    config = read_json(config_filename)
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


def test_date_range_generator():
    '''
    test create_date_range
    '''

    # DAYS
    start = '2010-01-01'
    end = '2010-01-30'
    drange = du.create_date_range(start, end, 'day')
    assert(len(drange) == 30)

    assert(drange[1] == '2010-01-02')
    assert(drange[-1] == end)

    start = '2010-01-01'
    end = '2010-12-31'
    drange = du.create_date_range(start, end, 'day')
    assert(len(drange) == 365)

    start = '2015-06-05'
    end = '2015-06-10'
    drange = du.create_date_range(start, end, 'day')
    assert(len(drange) == 6)

    # MONTHS
    start = '2010-01'
    end = '2010-01'
    drange = du.create_date_range(start, end, 'month')
    assert(len(drange) == 1)


    start = '2010-01'
    end = '2010-12'
    drange = du.create_date_range(start, end, 'month')
    assert(len(drange) == 12)

    assert(drange[1] == '2010-02')
    assert(drange[-1] == end)

    start = '2000-01'
    end = '2016-12'
    drange = du.create_date_range(start, end, 'month')
    assert(len(drange) == 204)

    assert(drange[1] == '2000-02')
    assert(drange[-1] == end)

    # YEARS
    start = '2010'
    end = '2015'
    drange = du.create_date_range(start, end, 'year')
    assert(len(drange) == 6)

    start = '1910'
    end = '2015'
    drange = du.create_date_range(start, end, 'year')
    assert(len(drange) == 106)
    assert(drange[-1] == end)

    # day_hour
    start = '2010-01-01'
    end = '2010-01-30'
    drange = du.create_date_range(start, end, 'day_hour')
    assert(len(drange) == 30 * 24)
    assert(drange[-1] == end + '+23')
