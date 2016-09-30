import urllib2
from flask import Flask
from flask_testing import TestCase
from mlab_api.app import app
from mlab_api.rest_api import api
from mlab_api.endpoints.locations import locations_ns
from mlab_api.endpoints.servers import server_asn_ns
from mlab_api.endpoints.debug import debug_ns
# from flask_testing import LiveServerTestCase


def check_for_fields(data, root, fields):
    assert(root in data)
    for field in fields:
        assert data[root][field] is not None, "{0} is not present in {1}".format(field, root)

def check_all_for_fields(results, root, fields):
    for row in results:
        check_for_fields(row, root, fields)

class TestApp(TestCase):

    # seems to have a problem with
    # trying to init_app mulitple times.
    init = False

    def create_app(self):
        if not TestApp.init:
            api.add_namespace(locations_ns)
            api.add_namespace(server_asn_ns)
            api.add_namespace(debug_ns)
            api.init_app(app)
            TestApp.init = True
        return app

    def test_debug_connection(self):
        response = self.client.get("/debug/connection")
        self.assertIsNotNone(response.json['tables'])

    def test_locations_children(self):
        location_key = 'nausks'
        response = self.client.get("/locations/{0}/children".format(location_key))
        self.assertIsNotNone(response.json['results'])
        assert(len(response.json['results']) > 0)

        meta_fields = ['id', 'client_region', 'client_location_key']
        check_all_for_fields(response.json['results'], 'meta', meta_fields)

        data_fields = ['last_year_test_count']
        check_for_fields(response.json['results'][0], 'data', data_fields)

    def test_locations_info(self):
        location_key = 'nausma'
        response = self.client.get("/locations/{0}/info".format(location_key))
        self.assertIsNotNone(response.json['data'])

        meta_fields = ['id', 'client_region', 'client_location_key']
        check_for_fields(response.json, 'meta', meta_fields)

        data_fields = ['last_year_test_count']
        check_for_fields(response.json, 'data', data_fields)

    def test_locations_metrics(self):
        location_key = 'nausma'
        time_aggs = ['day', 'month', 'year', 'day_hour', 'month_hour', 'year_hour']
        for time_agg in time_aggs:
            response = self.client.get("/locations/{0}/metrics?timebin={1}".format(location_key, time_agg))
            self.assertIsNotNone(response.json['results'])
            self.assertIsNotNone(response.json['meta'])
            self.assertIsNotNone(response.json['meta']['id'])
            assert(len(response.json['results']) > 0)

            meta_fields = ['id', 'client_location_key']
            check_for_fields(response.json, 'meta', meta_fields)

            result = response.json['results'][0]
            expected_fields = ['count', 'date']
            for key in expected_fields:
                self.assertIsNotNone(result[key])

    def test_locations_clients(self):
        location_key = 'nausmaboston'
        response = self.client.get("/locations/{0}/clients".format(location_key))
        self.assertIsNotNone(response.json['results'])
        results = response.json['results']

        meta_fields = ['client_asn_number', 'id']
        check_all_for_fields(results, 'meta', meta_fields)

        isp_nums = [r['meta']['client_asn_number'] for r in response.json['results']]
        assert('AS7922' in isp_nums)

    def test_locations_clients_metrics(self):
        location_key = 'nausmaboston'
        client_isp = 'AS7922'
        time_aggs = ['day', 'month', 'year', 'day_hour', 'month_hour', 'year_hour']
        for time_agg in time_aggs:
            response = self.client.get("/locations/{0}/clients/{1}/metrics?timebin={2}".format(location_key, client_isp, time_agg))
            self.assertIsNotNone(response.json['results'])
            self.assertIsNotNone(response.json['meta'])
            assert(len(response.json['results']) > 0)

            meta_fields = ['id', 'client_asn_number']
            for meta_field in meta_fields:
                self.assertIsNotNone(response.json['meta'][meta_field])

            result = response.json['results'][0]
            
            expected_fields = ['date']
            for key in expected_fields:
                self.assertIsNotNone(result[key])

    def test_locations_clients_info(self):
        location_key = 'nausmaboston'
        client_isp = 'AS7922'
        response = self.client.get("/locations/{0}/clients/{1}/info".format(location_key, client_isp))
        self.assertIsNotNone(response.json['data'])

        result = response.json
        expected_fields = [('meta', 'client_region'), ('meta', 'last_year_test_count'), ('data', 'last_year_download_speed_mbps_median')]
        for family, key in expected_fields:
            self.assertIsNotNone(result[family][key])

    def test_locations_search(self):
        location_key = 'kansascity'
        response = self.client.get("/locations/search?q={0}".format(location_key))
        self.assertIsNotNone(response.json['results'])
        assert(len(response.json['results']) > 0)
        # check for some fields
        result = response.json['results'][0]
        expected_fields = [('meta', 'location_key'), ('data', 'test_count')]
        for family, key in expected_fields:
            self.assertIsNotNone(result[family][key])

    def test_servers_search(self):
        search_key = 'a'
        response = self.client.get("/servers/search?q={0}".format(search_key))
        self.assertIsNotNone(response.json['results'])
        assert(len(response.json['results']) > 0)

        # check for some fields
        result = response.json['results'][0]
        expected_fields = [('meta', 'server_asn_name'), ('data', 'test_count')]
        for family, key in expected_fields:
            self.assertIsNotNone(result[family][key])

    def tearDown(self):
        pass
        # app = None
