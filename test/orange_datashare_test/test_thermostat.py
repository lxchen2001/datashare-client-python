import json
from http.client import OK
from unittest import TestCase

from orange_datashare.thermostat import ThermostatApi, ThermostatMode
from orange_datashare_test.abstract_test_case import AbstractTestCase
from orange_datashare_test.fake_requests import mock_api_response, load_resource_file


class ThermostatApiTest(TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()
        self.thermostat = ThermostatApi(self.client)

    def _test_mode(self, mode, temperature, end_date, expected_file):
        self.client.put.return_value = mock_api_response('/api/v2/users/-/commands/thermostat/mode',
                                                         OK,
                                                         None,
                                                         'thermostat', 'mode', 'PUT_response.json')
        expected_request = json.loads(load_resource_file('thermostat', 'mode', expected_file))
        self.thermostat.set_mode('-', ['thermostat-udi'], mode, temperature, end_date)
        self.client.put.assert_called_with(self.client.put.return_value.url, data=None, json=expected_request)

    def test_set_mode_with_timestamp(self):
        self._test_mode(ThermostatMode.ANTIFREEZE, 19.0, 1482316511.7452345, 'PUT_antifreeze_request.json')

    def test_set_mode_with_json_string(self):
        self._test_mode(ThermostatMode.MANUAL, 19.0, "2016-12-21T11:35:11.745Z", 'PUT_manual_request.json')

    def test_set_mode_without_date(self):
        self._test_mode(ThermostatMode.ENERGYSAVER, 19.0, None, 'PUT_energysaver_request.json')
