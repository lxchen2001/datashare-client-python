"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
import json
from orange_datashare.imported import ACCEPTED
from unittest import TestCase

from orange_datashare.command import CommandApi, ThermostatMode
from orange_datashare_test.abstract_test_case import AbstractTestCase
from orange_datashare_test.fake_requests import mock_api_response, load_resource_file


class CommandApiTest(TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()
        self.command = CommandApi(self.client)

    def _test_thermostat_mode(self, mode, temperature, end_date, expected_file):
        self.client.put.return_value = mock_api_response('/api/v2/users/-/commands/thermostat/mode',
                                                         ACCEPTED,
                                                         None,
                                                         'thermostat', 'mode', 'PUT_response.json')
        expected_request = json.loads(load_resource_file('thermostat', 'mode', expected_file))
        self.command.set_thermostat_mode('-', ['thermostat-udi'], mode, temperature, end_date)
        self.client.put.assert_called_with(self.client.put.return_value.url, data=None, json=expected_request,
                                           headers=self.DEFAULT_HEADERS)

    def _test_light_state(self, color, expected_file):
        self.client.put.return_value = mock_api_response('/api/v2/users/-/commands/light/state',
                                                         ACCEPTED,
                                                         None,
                                                         'light', 'state', 'PUT_response.json')
        expected_request = json.loads(load_resource_file('light', 'state', expected_file))
        self.command.set_light_state('-', ['light-udi'], True, color)
        self.client.put.assert_called_with(self.client.put.return_value.url, data=None, json=expected_request,
                                           headers=self.DEFAULT_HEADERS)

    def test_set_thermostat_mode_with_timestamp(self):
        self._test_thermostat_mode(ThermostatMode.ANTIFREEZE, 19.0, 1482316511.7452345, 'PUT_antifreeze_request.json')

    def test_set_thermostat_mode_with_json_string(self):
        self._test_thermostat_mode(ThermostatMode.MANUAL, 19.0, "2016-12-21T11:35:11.745Z", 'PUT_manual_request.json')

    def test_set_thermostat_mode_without_date(self):
        self._test_thermostat_mode(ThermostatMode.ENERGYSAVER, 19.0, None, 'PUT_energysaver_request.json')

    def test_set_light_state_by_rgb(self):
        self._test_light_state([1, 2, 3], 'PUT_rgb_request.json')

    def test_set_light_state_by_hsl(self):
        self._test_light_state([10.0, 0.5, 0.6], 'PUT_hsl_request.json')

    def test_set_light_state_by_hex(self):
        self._test_light_state("#FF5500", 'PUT_hex_request.json')
