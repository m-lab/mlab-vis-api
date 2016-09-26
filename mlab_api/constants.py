
FILTER_TYPES = ['locations', 'clients', 'servers']

TABLE_KEYS = {
    'locations': 'client_loc',
    'clients': 'client_asn',
    'servers': 'server_asn'
}

TIME_BINS = {
    'day': {'startdate': '2015-10-01', 'enddate': '2015-10-31'},
    'month': {'startdate': '2015-01', 'enddate': '2016-01'},
    'year': {'startdate': '2010', 'enddate': '2016'},
    'day_hour': {'startdate': '2015-10-01+0', 'enddate': '2015-11-01+0'},
    'month_hour': {'startdate': '2015-01', 'enddate': '2015-10'},
    'year_hour': {'startdate': '2015', 'enddate': '2016'}
}
