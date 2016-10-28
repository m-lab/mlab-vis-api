# -*- coding: utf-8 -*-
'''
Data class for accessing data for API calls.
'''
from mlab_api.data.base_data import Data
from mlab_api.constants import TABLE_KEYS
from mlab_api.data.table_config import get_table_config
from mlab_api.decorators import add_ids, add_id_value, add_id
import mlab_api.data.data_utils as du
import mlab_api.data.bigtable_utils as bt

class LocationData(Data):
    '''
    Connect to BigTable and pull down location data.
    '''

    @add_id_value()
    def get_location_info(self, location_id):
        '''
        Get info about specific location

        location_id = id string of location.
        '''

        table_config = get_table_config(self.table_configs,
                                        None,
                                        du.list_table('locations'))
        # add empty field to get child location in there
        location_key_fields = du.get_key_fields(["info", location_id], table_config)

        row_key = du.BIGTABLE_KEY_DELIM.join(location_key_fields)
        row = ""
        row = bt.get_row(table_config, self.get_pool(), row_key)

        return row

    @add_ids('parent_location_key')
    def get_location_children(self, location_id, type_filter=None):
        '''
        Return information about children regions of a location

        location_id = id string of location.
        type_filter = optionally restrict results to a location type.
        '''
        table_config = get_table_config(self.table_configs,
                                        None,
                                        du.list_table('locations'))
        location_key_fields = du.get_location_key_fields(location_id, table_config)

        location_key_field = du.BIGTABLE_KEY_DELIM.join(location_key_fields)

        results = []
        results = bt.scan_table(table_config, self.get_pool(), prefix=location_key_field)
        if type_filter:
            results = [r for r in results if r['meta']['type'] == type_filter]

        return {"results": results}

    @add_ids('client_asn_number')
    def get_location_clients(self, location_id, include_data):
        '''
        Get list and info of client isps for a location

        location_id = id string of location.
        include_data = boolean indicating whether to include data attributes in results or not.
        '''
        return self.get_list_data(location_id, 'locations', 'clients', include_data)


    @add_ids('server_asn_number')
    def get_location_servers(self, location_id, include_data):
        '''
        Get list and info of server isps for a location

        location_id = id string of location.
        include_data = boolean indicating whether to include data attributes in results or not.
        '''
        return self.get_list_data(location_id, 'locations', 'servers', include_data)

    @add_id('client_asn_number')
    def get_location_client_isp_info(self, location_id, client_id):
        '''
        Get static information about

        location_id = id string of location.
        client_id = id string of client.
        '''
        config_id = du.list_table('clients', 'locations')
        table_config = get_table_config(self.table_configs, None, config_id)

        key_fields = du.get_key_fields([location_id, client_id], table_config)

        row_key = du.BIGTABLE_KEY_DELIM.join(key_fields)

        results = []
        results = bt.get_row(table_config, self.get_pool(), row_key)

        return results

    def get_location_metrics(self, location_id, timebin, starttime, endtime):
        '''
        Get data for specific location at a specific
        frequency between start and stop times.

        location_id = id string of location.
        timebin = time aggregation key.
        starttime = start time for metric query.
        endtime = end time for metric query.
        '''

        table_config = get_table_config(self.table_configs, timebin, TABLE_KEYS["locations"])

        location_key_fields = du.get_location_key_fields(location_id, table_config)
        formatted = bt.get_time_metric_results(location_key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "locations")

        # set the ID to be the location ID
        if formatted['meta']:
            formatted["meta"]["id"] = location_id

        return formatted

    def get_location_client_metrics(self, location_id, client_id,
                                        timebin, starttime, endtime):
        '''
        Get data for specific location + client at a specific
        frequency between start and stop times for a
        specific client ISP.

        location_id = id string of location.
        client_id = id of client.
        timebin = time aggregation key.
        starttime = start time for metric query.
        endtime = end time for metric query.
        '''
        # Create Row Key
        agg_name = TABLE_KEYS["clients"] + '_' + TABLE_KEYS["locations"]

        table_config = get_table_config(self.table_configs, timebin, agg_name)

        key_fields = du.get_key_fields([client_id, location_id], table_config)
        formatted = bt.get_time_metric_results(key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "locations_clients")

        # set the ID to be the Client ISP ID
        if formatted['meta']:
            formatted["meta"]["id"] = "_".join([location_id, client_id])

        return formatted

    def get_location_server_metrics(self, location_id, server_id,
                                        timebin, starttime, endtime):
        '''
        Get data for specific location + server at a specific
        frequency between start and stop times for a
        specific client ISP.

        location_id = id string of location.
        server_id = id of server.
        timebin = time aggregation key.
        starttime = start time for metric query.
        endtime = end time for metric query.
        '''
        # Create Row Key
        agg_name = TABLE_KEYS["servers"] + '_' + TABLE_KEYS["locations"]

        table_config = get_table_config(self.table_configs, timebin, agg_name)

        # TODO: the direction of the keys don't match the table name
        key_fields = du.get_key_fields([location_id, server_id], table_config)
        formatted = bt.get_time_metric_results(key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "locations_servers")

        # set the ID to be the Client ISP ID
        if formatted['meta']:
            formatted["meta"]["id"] = "_".join([location_id, server_id])

        return formatted

    def get_location_client_server_metrics(self, location_id, client_id, server_id,
                                        timebin, starttime, endtime):
        '''
        Get data for specific location + client + server at a specific
        frequency between start and stop times for a
        specific client ISP.

        location_id = id string of location.
        client_id = id of client.
        server_id = id of server.
        timebin = time aggregation key.
        starttime = start time for metric query.
        endtime = end time for metric query.
        '''
        # Create Row Key
        agg_name = "{0}_{1}_{2}".format(TABLE_KEYS["servers"], TABLE_KEYS["clients"], TABLE_KEYS["locations"])

        table_config = get_table_config(self.table_configs, timebin, agg_name)

        key_fields = du.get_key_fields([location_id, client_id, server_id], table_config)
        formatted = bt.get_time_metric_results(key_fields, self.get_pool(), timebin, starttime, endtime, table_config, "locations_clients_servers")

        # set the ID to be the Client ISP ID
        if formatted['meta']:
            formatted["meta"]["id"] = "_".join([location_id, client_id, server_id])

        return formatted
