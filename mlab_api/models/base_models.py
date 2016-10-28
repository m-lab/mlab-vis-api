# -*- coding: utf-8 -*-
'''
Base models that can be nested or extended to create those used in responses
'''
from flask_restplus import fields
from mlab_api.rest_api import api
from mlab_api.id_utils import location_id, location_client_id, location_server_id, \
    location_client_server_id, client_id, server_id, client_server_id


# ----------------------------------------------------
# Generic Data Fields
# ----------------------------------------------------

search_data_fields = api.model('Search Data', {
    'last_three_months_test_count': fields.Integer(description="Test counts over last 3 months."),
    'last_six_months_test_count': fields.Integer(description="Test counts in last six months"),
    'last_year_test_count': fields.Integer(description="Test counts in last year"),
    'test_count': fields.Integer(description="Test counts over entire MLab dataset"),
})

# Unfortunately, currently some models include test count in meta and some do it in data
# (e.g., see location info vs location+client info). Ideally this gets fixed at some point.
search_meta_fields = api.model('Search Meta', {
    'last_three_months_test_count': fields.Integer(description="Test counts over last 3 months."),
    'last_six_months_test_count': fields.Integer(description="Test counts in last six months"),
    'last_year_test_count': fields.Integer(description="Test counts in last year"),
    'test_count': fields.Integer(description="Test counts over entire MLab dataset"),
})

metric_data_fields = api.model('Metric Data', {
    'count': fields.Integer(description="Test counts for time period."),
    'rtt_avg': fields.Float(description="Average round trip time"),
    'retransmit_avg': fields.Float(description="Average retransmit rate."),
    'download_speed_mbps_median': fields.Float(description="Median Download Speed."),
    'upload_speed_mbps_median': fields.Float(description="Median Upload Speed."),
    'hour': fields.String(description="Hour Aggregation, if requested by hour."),
    'date': fields.String(description="Date for time period")
})


# ----------------------------------------------------
# Servers
# ----------------------------------------------------
# Server: meta
server_meta_fields = api.model('Server Meta', {
    'server_asn_number': fields.String(description="Server ASN Number"),
    'server_asn_name': fields.Raw(description="Server ASN Name"),
    'id': fields.String(description="Server ID", attribute=server_id)
})

# Server: search meta
server_search_meta_fields = search_meta_fields.extend('Server Search Meta', server_meta_fields)
api.models[server_search_meta_fields.name] = server_search_meta_fields # Register extended model manually


# ----------------------------------------------------
# Clients
# ----------------------------------------------------
# Client: meta
client_meta_fields = api.model('Client Meta', {
    'client_asn_number': fields.String(description="Client ASN Number"),
    'client_asn_name': fields.Raw(description="Client ASN Name"),
    'id': fields.String(description="Client ID", attribute=client_id)
})

# Client: search meta
client_search_meta_fields = search_meta_fields.extend('Client Search Meta', client_meta_fields)
api.models[client_search_meta_fields.name] = client_search_meta_fields # Register extended model manually


# ----------------------------------------------------
# Clients + Servers
# ----------------------------------------------------
client_server_meta_fields = client_meta_fields.extend('Clients+Servers Meta (no ID)',
    server_search_meta_fields).extend('Clients+Servers Meta', {
        'id': fields.String(description="Clients+Servers Id", attribute=client_server_id),
    })
api.models[client_server_meta_fields.name] = client_server_meta_fields # Register extended model manually


# ----------------------------------------------------
# Locations
# ----------------------------------------------------
# Location: meta
location_meta_fields = api.model('Location Meta', {
    'id': fields.Raw(description="Location id", attribute=location_id),
    'type': fields.String(description="Location type. city, region, country, or continent."),
    'location_key': fields.Raw(description="Key of location.", attribute=location_id),
    'client_continent': fields.String(description="Continent of Location."),
    'client_continent_code': fields.String(description="Continent code of Location."),
    'client_country': fields.String(description="Country of Location."),
    'client_country_code': fields.String(description="Country code of Location."),
    'client_region': fields.String(description="Region of Location."),
    'client_region_code': fields.String(description="Region code of Location."),
    'client_city': fields.Raw(description="Name of city, if location is a city.")
})

# Location Search: meta
location_search_meta_fields = search_meta_fields.extend('Location Search Meta', location_meta_fields)
api.models[location_search_meta_fields.name] = location_search_meta_fields # Register extended model manually

# Location Info: data
location_info_data_fields = api.model('Location Info Data', {
    'last_year_download_speed_mbps_median': fields.Float,
    'last_year_download_speed_mbps_avg': fields.Float,
    'last_year_download_speed_mbps_min': fields.Float,
    'last_year_download_speed_mbps_max': fields.Float,
    'last_year_download_speed_mbps_stddev': fields.Float,
    'last_year_download_speed_mbps_bins': fields.List(fields.Integer, description="Distribution of download speeds"),
    'last_year_upload_speed_mbps_median': fields.Float,
    'last_year_upload_speed_mbps_avg': fields.Float,
    'last_year_upload_speed_mbps_min': fields.Float,
    'last_year_upload_speed_mbps_max': fields.Float,
    'last_year_upload_speed_mbps_stddev': fields.Float,
    'last_year_upload_speed_mbps_bins': fields.List(fields.Integer, description="Distribution of upload speeds"),
    'last_year_test_count': fields.Integer(description="Test counts in last year"),
    'last_year_rtt_avg': fields.Float,
    'last_year_rtt_avg_bins': fields.List(fields.Integer, description="Distribution of RTT"),
    'last_year_retransmit_avg': fields.Float,
    'last_year_packet_retransmit_rate_bins': fields.List(fields.Integer, description="Distribution of Retransmit rate"),

    'last_three_months_download_speed_mbps_median': fields.Float,
    'last_three_months_download_speed_mbps_avg': fields.Float,
    'last_three_months_download_speed_mbps_min': fields.Float,
    'last_three_months_download_speed_mbps_max': fields.Float,
    'last_three_months_download_speed_mbps_stddev': fields.Float,
    'last_three_months_download_speed_mbps_bins': fields.List(fields.Integer, description="Distribution of download speeds"),
    'last_three_months_upload_speed_mbps_median': fields.Float,
    'last_three_months_upload_speed_mbps_avg': fields.Float,
    'last_three_months_upload_speed_mbps_min': fields.Float,
    'last_three_months_upload_speed_mbps_max': fields.Float,
    'last_three_months_upload_speed_mbps_stddev': fields.Float,
    'last_three_months_upload_speed_mbps_bins': fields.List(fields.Integer, description="Distribution of upload speeds"),
    'last_three_months_test_count': fields.Integer(description="Test counts in last three months"),
    'last_three_months_rtt_avg': fields.Float,
    'last_three_months_rtt_avg_bins': fields.List(fields.Integer, description="Distribution of RTT"),
    'last_three_months_retransmit_avg': fields.Float,
    'last_three_months_packet_retransmit_rate_bins': fields.List(fields.Integer, description="Distribution of Retransmit rate"),

    'last_six_months_download_speed_mbps_median': fields.Float,
    'last_six_months_download_speed_mbps_avg': fields.Float,
    'last_six_months_download_speed_mbps_min': fields.Float,
    'last_six_months_download_speed_mbps_max': fields.Float,
    'last_six_months_download_speed_mbps_stddev': fields.Float,
    'last_six_months_download_speed_mbps_bins': fields.List(fields.Integer, description="Distribution of download speeds"),
    'last_six_months_upload_speed_mbps_median': fields.Float,
    'last_six_months_upload_speed_mbps_avg': fields.Float,
    'last_six_months_upload_speed_mbps_min': fields.Float,
    'last_six_months_upload_speed_mbps_max': fields.Float,
    'last_six_months_upload_speed_mbps_stddev': fields.Float,
    'last_six_months_upload_speed_mbps_bins': fields.List(fields.Integer, description="Distribution of upload speeds"),
    'last_six_months_test_count': fields.Integer(description="Test counts in last six months"),
    'last_six_months_rtt_avg': fields.Float,
    'last_six_months_rtt_avg_bins': fields.List(fields.Integer, description="Distribution of RTT"),
    'last_six_months_retransmit_avg': fields.Float,
    'last_six_months_packet_retransmit_rate_bins': fields.List(fields.Integer, description="Distribution of Retransmit rate"),
})

# ----------------------------------------------------
# Locations + Clients
# ----------------------------------------------------
location_client_meta_fields = location_meta_fields.extend('Location+Clients Meta (no ID)',
    client_search_meta_fields).extend('Location+Clients Meta', {
        'id': fields.Raw(description="Location+Clients Id", attribute=location_client_id),
    })
api.models[location_client_meta_fields.name] = location_client_meta_fields # Register extended model manually


# ----------------------------------------------------
# Locations + Servers
# ----------------------------------------------------
location_server_meta_fields = location_meta_fields.extend('Location+Servers Meta (no ID)',
    server_search_meta_fields).extend('Location+Servers Meta', {
        'id': fields.Raw(description="Location+Servers Id", attribute=location_server_id),
    })
api.models[location_server_meta_fields.name] = location_server_meta_fields # Register extended model manually

# ----------------------------------------------------
# Locations + Clients + Servers
# ----------------------------------------------------
location_client_server_meta_fields = location_client_meta_fields.extend('Location+Clients+Servers Meta (no ID)',
    server_search_meta_fields).extend('Location+Clients+Servers Meta', {
        'id': fields.Raw(description="Location+Clients+Servers Id", attribute=location_client_server_id),
    })
api.models[location_client_server_meta_fields.name] = location_client_server_meta_fields # Register extended model manually
