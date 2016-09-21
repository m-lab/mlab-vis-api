# -*- coding: utf-8 -*-
'''
Base Data Class
'''
CONSTS = {
    "CLIENT_LOCATION_KEY": 'client_loc',
    "CLIENT_ASN_KEY": 'client_asn',
    "SERVER_ASN_KEY": 'server_asn'
}

class Data(object):
    '''
    Connect to BigTable and pull down data.
    '''

    def __init__(self, table_configs, connection_pool):
        '''
        Constructor.
        '''
        self.connection_pool = connection_pool
        self.table_configs = table_configs


    def get_pool(self):
        '''
        Return Bigtable connection pool
        '''
        return self.connection_pool
