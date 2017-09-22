# -*- coding: utf-8 -*-
'''
Helpers to get IDs properly marshaled
'''


def location_id(location):
    '''
    Create ID for locations
    '''
    if location is None:
        location = {}
    if 'location_key' in location:
        return location['location_key']
    if 'client_location_key' in location:
        return location['client_location_key']
    if 'child_location_key' in location:
        return location['child_location_key']
    if 'id' in location:
        return location['id']

    return None


def client_id(client):
    '''
    Create ID for clients
    '''
    if client is None:
        client = {}
    if 'client_asn_number' in client:
        return client['client_asn_number']
    return None

def server_id(server):
    '''
    Create ID for servers
    '''
    if server is None:
        server = {}
    if 'server_asn_number' in server:
        return server['server_asn_number']
    return None

def location_client_id(location_client):
    '''
    Create composite ID for locations + clients
    '''
    return '%s_%s' % (location_id(location_client), client_id(location_client))


def location_server_id(location_server):
    '''
    Create composite ID for locations + servers
    '''
    return '%s_%s' % (location_id(location_server), server_id(location_server))

def location_client_server_id(location_client_server):
    '''
    Create composite ID for locations + clients + servers
    '''
    return '%s_%s_%s' % (location_id(location_client_server),
                         client_id(location_client_server),
                         server_id(location_client_server))

def client_server_id(client_server):
    '''
    Create composite ID for clients + servers
    '''
    return '%s_%s' % (client_id(client_server), server_id(client_server))
