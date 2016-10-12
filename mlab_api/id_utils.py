
def location_client_id(d):
    '''
    Create composite ID for locations + clients
    '''
    return '%s_%s' % (d['location_key'] if 'location_key' in d else d['client_location_key'],
                      d['client_asn_number'])
