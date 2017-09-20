# -*- coding: utf-8 -*-
'''
Base models that can be nested or extended to create those used in responses
'''
from flask_restplus import fields
from mlab_api.rest_api import API
from mlab_api.id_utils import location_id, location_client_id, \
    location_server_id, location_client_server_id, client_id, server_id, \
    client_server_id


# ----------------------------------------------------
# Generic Data Fields
# ----------------------------------------------------

SEARCH_DATA_FIELDS = API.model('Search Data', {
    'last_three_months_test_count': fields.Integer(
        description="Test counts over last 3 months."),
    'last_six_months_test_count': fields.Integer(
        description="Test counts in last six months"),
    'last_year_test_count': fields.Integer(
        description="Test counts in last year"),
    'test_count': fields.Integer(
        description="Test counts over entire MLab dataset"),
})

# Unfortunately, currently some models include test count in meta and some do
# it in data (e.g., see location info vs location+client info).
# Ideally this gets fixed at some point.
SEARCH_META_FIELDS = API.model('Search Meta', {
    'last_three_months_test_count': fields.Integer(
        description="Test counts over last 3 months."),
    'last_six_months_test_count': fields.Integer(
        description="Test counts in last six months"),
    'last_year_test_count': fields.Integer(
        description="Test counts in last year"),
    'test_count': fields.Integer(
        description="Test counts over entire MLab dataset"),
})

METRIC_META_FIELDS = API.model('Metric Data', {
    'count': fields.Integer(description="Test counts for time period."),
    'rtt_avg': fields.Float(description="Average round trip time"),
    'retransmit_avg': fields.Float(description="Average retransmit rate."),
    'download_speed_mbps_median': fields.Float(
        description="Median Download Speed."),
    'upload_speed_mbps_median': fields.Float(
        description="Median Upload Speed."),
    'hour': fields.String(
        description="Hour Aggregation, if requested by hour."),
    'date': fields.String(description="Date for time period")
})


# ----------------------------------------------------
# Servers
# ----------------------------------------------------
# Server: meta
SERVER_META_FIELDS = API.model('Server Meta', {
    'server_asn_number': fields.String(description="Server ASN Number"),
    'server_asn_name': fields.Raw(description="Server ASN Name"),
    'id': fields.String(description="Server ID", attribute=server_id)
})

# Server: search meta
SERVER_SEARCH_META_FIELDS = SEARCH_META_FIELDS.extend('Server Search Meta',
                                                      SERVER_META_FIELDS)
# Register extended model manually
API.models[SERVER_SEARCH_META_FIELDS.name] = SERVER_SEARCH_META_FIELDS


# ----------------------------------------------------
# Clients
# ----------------------------------------------------
# Client: meta
CLIENT_META_FIELDS = API.model('Client Meta', {
    'client_asn_number': fields.String(description="Client ASN Number"),
    'client_asn_name': fields.Raw(description="Client ASN Name"),
    'id': fields.String(description="Client ID", attribute=client_id)
})

# Client: search meta
CLIENT_SEARCH_META_FIELDS = SEARCH_META_FIELDS.extend('Client Search Meta',
                                                      CLIENT_META_FIELDS)
# Register extended model manually
API.models[CLIENT_SEARCH_META_FIELDS.name] = CLIENT_SEARCH_META_FIELDS


# ----------------------------------------------------
# Clients + Servers
# ----------------------------------------------------
CLIENT_SERVER_META_FIELDS = CLIENT_META_FIELDS.extend(
    'Clients+Servers Meta (no ID)',
    SERVER_SEARCH_META_FIELDS).extend('Clients+Servers Meta', {
        'id': fields.String(description="Clients+Servers Id",
                            attribute=client_server_id),
    })
# Register extended model manually
API.models[CLIENT_SEARCH_META_FIELDS.name] = CLIENT_SERVER_META_FIELDS


# ----------------------------------------------------
# Locations
# ----------------------------------------------------
# Location: meta
LOCATION_META_FIELDS = API.model('Location Meta', {
    'id': fields.Raw(description="Location id", attribute=location_id),
    'type': fields.String(
        description="Location type. city, region, country, or continent."),
    'location_key': fields.Raw(
        description="Key of location.", attribute=location_id),
    'client_continent': fields.String(
        description="Continent of Location."),
    'client_continent_code': fields.String(
        description="Continent code of Location."),
    'client_country': fields.String(description="Country of Location."),
    'client_country_code': fields.String(
        description="Country code of Location."),
    'client_region': fields.String(description="Region of Location."),
    'client_region_code': fields.String(description="Region code of Location."),
    'client_city': fields.Raw(
        description="Name of city, if location is a city.")
})

# Location Search: meta
LOCATION_SEARCH_META_FIELDS = SEARCH_META_FIELDS.extend(
    'Location Search Meta', LOCATION_META_FIELDS)
# Register extended model manually
API.models[LOCATION_SEARCH_META_FIELDS.name] = LOCATION_SEARCH_META_FIELDS

# Location Info: data
LOCATION_INFO_DATA_FIELDS = API.model('Location Info Data', {
    'last_year_download_speed_mbps_median': fields.Float,
    'last_year_download_speed_mbps_avg': fields.Float,
    'last_year_download_speed_mbps_min': fields.Float,
    'last_year_download_speed_mbps_max': fields.Float,
    'last_year_download_speed_mbps_stddev': fields.Float,
    'last_year_download_speed_mbps_bins': fields.List(
        fields.Integer, description="Distribution of download speeds"),
    'last_year_upload_speed_mbps_median': fields.Float,
    'last_year_upload_speed_mbps_avg': fields.Float,
    'last_year_upload_speed_mbps_min': fields.Float,
    'last_year_upload_speed_mbps_max': fields.Float,
    'last_year_upload_speed_mbps_stddev': fields.Float,
    'last_year_upload_speed_mbps_bins': fields.List(
        fields.Integer, description="Distribution of upload speeds"),
    'last_year_test_count': fields.Integer(
        description="Test counts in last year"),
    'last_year_rtt_avg': fields.Float,
    'last_year_rtt_avg_bins': fields.List(
        fields.Integer, description="Distribution of RTT"),
    'last_year_retransmit_avg': fields.Float,
    'last_year_packet_retransmit_rate_bins': fields.List(
        fields.Integer, description="Distribution of Retransmit rate"),
    'last_three_months_download_speed_mbps_median': fields.Float,
    'last_three_months_download_speed_mbps_avg': fields.Float,
    'last_three_months_download_speed_mbps_min': fields.Float,
    'last_three_months_download_speed_mbps_max': fields.Float,
    'last_three_months_download_speed_mbps_stddev': fields.Float,
    'last_three_months_download_speed_mbps_bins': fields.List(
        fields.Integer, description="Distribution of download speeds"),
    'last_three_months_upload_speed_mbps_median': fields.Float,
    'last_three_months_upload_speed_mbps_avg': fields.Float,
    'last_three_months_upload_speed_mbps_min': fields.Float,
    'last_three_months_upload_speed_mbps_max': fields.Float,
    'last_three_months_upload_speed_mbps_stddev': fields.Float,
    'last_three_months_upload_speed_mbps_bins': fields.List(
        fields.Integer, description="Distribution of upload speeds"),
    'last_three_months_test_count': fields.Integer(
        description="Test counts in last three months"),
    'last_three_months_rtt_avg': fields.Float,
    'last_three_months_rtt_avg_bins': fields.List(
        fields.Integer, description="Distribution of RTT"),
    'last_three_months_retransmit_avg': fields.Float,
    'last_three_months_packet_retransmit_rate_bins': fields.List(
        fields.Integer, description="Distribution of Retransmit rate"),

    'last_six_months_download_speed_mbps_median': fields.Float,
    'last_six_months_download_speed_mbps_avg': fields.Float,
    'last_six_months_download_speed_mbps_min': fields.Float,
    'last_six_months_download_speed_mbps_max': fields.Float,
    'last_six_months_download_speed_mbps_stddev': fields.Float,
    'last_six_months_download_speed_mbps_bins': fields.List(
        fields.Integer, description="Distribution of download speeds"),
    'last_six_months_upload_speed_mbps_median': fields.Float,
    'last_six_months_upload_speed_mbps_avg': fields.Float,
    'last_six_months_upload_speed_mbps_min': fields.Float,
    'last_six_months_upload_speed_mbps_max': fields.Float,
    'last_six_months_upload_speed_mbps_stddev': fields.Float,
    'last_six_months_upload_speed_mbps_bins': fields.List(
        fields.Integer, description="Distribution of upload speeds"),
    'last_six_months_test_count': fields.Integer(
        description="Test counts in last six months"),
    'last_six_months_rtt_avg': fields.Float,
    'last_six_months_rtt_avg_bins': fields.List(
        fields.Integer, description="Distribution of RTT"),
    'last_six_months_retransmit_avg': fields.Float,
    'last_six_months_packet_retransmit_rate_bins': fields.List(
        fields.Integer, description="Distribution of Retransmit rate"),
})

# ----------------------------------------------------
# Locations + Clients
# ----------------------------------------------------
LOCATION_CLIENT_META_FIELDS = LOCATION_META_FIELDS.extend(
    'Location+Clients Meta (no ID)',
    CLIENT_SEARCH_META_FIELDS).extend('Location+Clients Meta', {
        'id': fields.Raw(description="Location+Clients Id",
                         attribute=location_client_id),
    })
# Register extended model manually
API.models[LOCATION_CLIENT_META_FIELDS.name] = LOCATION_CLIENT_META_FIELDS


# ----------------------------------------------------
# Locations + Servers
# ----------------------------------------------------
LOCATION_SERVER_META_FIELDS = LOCATION_META_FIELDS.extend(
    'Location+Servers Meta (no ID)',
    SERVER_SEARCH_META_FIELDS).extend('Location+Servers Meta', {
        'id': fields.Raw(description="Location+Servers Id",
                         attribute=location_server_id),
    })
# Register extended model manually
API.models[LOCATION_SERVER_META_FIELDS.name] = LOCATION_SERVER_META_FIELDS

# ----------------------------------------------------
# Locations + Clients + Servers
# ----------------------------------------------------
LOCATION_CLIENT_SERVER_META_FIELDS = LOCATION_CLIENT_META_FIELDS.extend(
    'Location+Clients+Servers Meta (no ID)',
    SERVER_SEARCH_META_FIELDS).extend('Location+Clients+Servers Meta', {
        'id': fields.Raw(description="Location+Clients+Servers Id",
                         attribute=location_client_server_id),
    })
# Register extended model manually
API.models[
    LOCATION_CLIENT_SERVER_META_FIELDS.name
] = LOCATION_CLIENT_SERVER_META_FIELDS
