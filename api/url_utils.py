
def get_time_window(args, time_aggregation, defaults):
    '''
    Returns starttime and endtime specified by args.
    If no value supplied, finds default value from defaults
    '''
    starttime = args.get('starttime', '')
    if (len(starttime) == 0) and (time_aggregation in defaults):
        starttime = defaults[time_aggregation]['starttime']

    endtime = args.get('endtime', '')
    if (len(endtime) == 0) and (time_aggregation in defaults):
        endtime = defaults[time_aggregation]['endtime']

    return (starttime, endtime)

def format_search_query(search_string):
    return search_string.lower().replace(" ", "")
