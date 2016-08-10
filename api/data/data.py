'''
Data class for accessing data for API calls.
'''
from __future__ import print_function
import struct
import logging

from gcloud import bigtable
from gcloud.bigtable import happybase

from oauth2client.client import GoogleCredentials
from table_config import get_table_config

URL_KEY_DELIM = "+"
BIGTABLE_KEY_DELIM = "|"


class Data(object):
    '''
    Deal with data things
    '''

    def __init__(self, app_config, table_configs):
        '''
        Constructor.
        '''
        self.connection = self.init_connection(app_config)
        self.table_configs = table_configs

    @staticmethod
    def init_connection(app_config):
        '''
        Setup Connection
        From the documentation:
        Creating a Connection object is a heavyweight operation;
         you should create a single Connection and
         share it among threads in your application.
        '''

        credentials = GoogleCredentials.get_application_default()
        connection = None

        if 'GOOGLE_PROJECT_ID' and 'BIGTABLE_INSTANCE' in app_config:
            try:
                client = bigtable.Client(project=app_config['GOOGLE_PROJECT_ID'],
                                         admin=True, credentials=credentials)

                instance = client.instance(app_config['BIGTABLE_INSTANCE'])

                connection = happybase.Connection(instance=instance)
            except Exception as err:  #pylint: disable=W0703
                logging.exception("ERROR: Could not make connection")
                print(err)
        else:
            print('WARNING: no connection made')
        return connection

    def get_connection(self):
        '''
        Returns current connection
        '''
        return self.connection

    @staticmethod
    def get_location_type(location_id):
        '''
        gets location type based on number of location fields
        '''
        location_fields = location_id.split(URL_KEY_DELIM)

        if len(location_fields) == 4:
            return 'client_city'
        elif len(location_fields) == 3:
            return 'client_region'
        elif len(location_fields) == 2:
            return 'client_country'
        elif len(location_fields) == 1:
            return 'client_continent'
        else:
            return 'unknown'


    @staticmethod
    def get_location_key_fields(location_id, table_config):
        '''
        Returns an array of strings representing the portions of the  row
        key for the location fields
        '''

        location_fields = location_id.split(URL_KEY_DELIM)
        location_key_fields = []
        for index, field in enumerate(location_fields):
            field_config = table_config['row_keys'][index]
            key_length = field_config['length']
            location_key_fields.append(field.ljust(key_length))

        return location_key_fields

    @staticmethod
    def get_time_key_fields(time_value, time_aggregation, table_config):
        '''
        Returns an array of strings representing the portions of the  row
        key for the time fields
        '''

        times = time_value.split(URL_KEY_DELIM)

        time_key_fields = []
        field_names = ['date']
        if 'hour' in time_aggregation:
            field_names.append('hour')
            if len(times) == 1:
                # we are missing an hour value
                times.append('0')

        for index, field_name in enumerate(field_names):
            field_config = [x for x in table_config['row_keys'] if x['name'] == field_name][0]
            key_length = field_config['length']
            time_key_fields.append(times[index].ljust(key_length))

        return time_key_fields

    @staticmethod
    def get_client_isp_fields(client_isp_id, table_config):
        '''
        Returns an array of strings representing portions of the row
        key for the Client ISP

        Args:
            client_isp_id - ASN Number
        '''

        client_parts = client_isp_id.split(URL_KEY_DELIM)
        client_isp_fields = []
        field_names = ['client_asn_number']

        for index, field_name in enumerate(field_names):
            field_config = [x for x in table_config['row_keys'] if x['name'] == field_name][0]
            key_length = field_config['length']
            client_isp_fields.append(client_parts[index].ljust(key_length))

        return client_isp_fields


    @staticmethod
    def decode(value, col_config):
        '''
        TODO
        '''
        new_value = value
        col_type = col_config['type']
        if col_type == 'double':
            try:
                new_value = round(struct.unpack('>d', value)[0], 3)
            except Exception as err:  #pylint: disable=W0703
                logging.exception("Double Conversion Error")
                logging.exception(str(err))
                new_value = None
        elif col_type == 'integer':
            try:
                new_value = int(value)
            except Exception as err:  #pylint: disable=W0703
                logging.exception("Integer Conversion Error")
                logging.exception(str(err))
                new_value = None
        else:
            try:
                new_value = value.encode('utf-8')
            except Exception as err:  #pylint: disable=W0703
                logging.exception("String Conversion Error")
                logging.exception(str(err))
                new_value = None
        return new_value

    @staticmethod
    def parse_data(data, col_configs):
        '''
        TODO
        '''
        parsed = {'data':{}, 'meta':{}}
        for key, value in data.iteritems():
            (family, name) = key.split(":")
            decoded_value = Data.decode(value, col_configs[name])
            parsed[family][name] = decoded_value

        return parsed

    @staticmethod
    def format_metrics(raw_data):
        '''
        Convert metric raw data list into format to send back to client
        '''
        results = {"metrics": [], "meta":{}}
        # Meta can be taken from first result

        formated_metrics = []
        for metric in raw_data:
            # special cases for date and hour
            if 'date' in metric['meta']:
                metric['data']['date'] = metric['meta']['date']
            if 'hour' in metric['meta']:
                metric['data']['hour'] = metric['meta']['hour']
            formated_metrics.append(metric['data'])
        results["metrics"] = formated_metrics

        if len(raw_data) > 0:
            meta = raw_data[0]["meta"]
            meta.pop('date', None)
            meta.pop('hour', None)

            results["meta"] = meta

        return results



    def close(self):
        '''
        Close connection
        '''
        if self.connection:
            self.connection.close()


    def get_location_metrics(self, location_id, time_aggregation, starttime, endtime):
        '''
        Get data for specific location at a specific
        frequency between start and stop times.
        '''

        location_type = self.get_location_type(location_id)

        table_config = get_table_config(self.table_configs,
                                        time_aggregation,
                                        location_type)


        location_key_fields = self.get_location_key_fields(location_id, table_config)

        starttime_fields = self.get_time_key_fields(starttime, time_aggregation, table_config)
        endtime_fields = self.get_time_key_fields(endtime, time_aggregation, table_config)

        start_key = BIGTABLE_KEY_DELIM.join(location_key_fields + starttime_fields)
        end_key = BIGTABLE_KEY_DELIM.join(location_key_fields + endtime_fields)

        table_id = table_config['bigtable_table_name']
        table = self.connection.table(table_id)

        print("querying: {0}".format(table_id))
        print("start_key: {0}".format(start_key))
        print("end_key: {0}".format(end_key))

        # HERE IS THE BIGTABLE QUERY
        results = []
        for _, data in table.scan(row_start=start_key, row_stop=end_key):
            results.append(self.parse_data(data, table_config.columns))
        return self.format_metrics(results)


    def get_location_client_isp_metrics(self, location_id, client_isp_id,
                                        time_aggregation, starttime, endtime):
        '''
        Get data for specific location at a specific
        frequency between start and stop times for a
        specific client ISP.

        TODO: currently only works for cities
        '''
        # Create Row Key

        location_type = self.get_location_type(location_id)
        agg_name = 'client_asn_number' + '_' + location_type

        table_config = get_table_config(self.table_configs,
                                        time_aggregation,
                                        agg_name)

        location_key_fields = self.get_location_key_fields(location_id, table_config)

        client_isp_fields = self.get_client_isp_fields(client_isp_id, table_config)

        starttime_fields = self.get_time_key_fields(starttime, time_aggregation, table_config)
        endtime_fields = self.get_time_key_fields(endtime, time_aggregation, table_config)

        # Start and End -- Row Keys
        start_key = BIGTABLE_KEY_DELIM.join(location_key_fields +
                                            client_isp_fields +
                                            starttime_fields)

        end_key = BIGTABLE_KEY_DELIM.join(location_key_fields +
                                          client_isp_fields +
                                          endtime_fields)

        # Prepare to query the table
        table_id = table_config['bigtable_table_name']
        table = self.connection.table(table_id)

        print("querying: {0}".format(table_id))
        print("start_key: {0}".format(start_key))
        print("end_key: {0}".format(end_key))


        # HERE IS THE BIGTABLE QUERY
        results = []
        for _, data in table.scan(row_start=start_key, row_stop=end_key):
            results.append(self.parse_data(data, table_config.columns))
        # format output for API
        return self.format_metrics(results)

    def get_location_search(self, location_query):
        '''
        API for location search
        '''
        table_config = get_table_config(self.table_configs,
                                        None,
                                        'location_search')

        table_id = table_config['bigtable_table_name']
        table = self.connection.table(table_id)
        print("querying: {0}".format(table_id))
        print("start_key: {0}".format(location_query))

        key_prefix = location_query

        # HERE IS THE BIGTABLE QUERY
        results = []
        for _, data in table.scan(row_prefix=key_prefix):
            results.append(self.parse_data(data, table_config.columns))
        # sort based on test_count
        sorted_results = sorted(results, key=lambda k: k['data']['test_count'], reverse=True)
        return sorted_results
