"""
Copyright (C) 2016 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
import json
from http.client import OK
from unittest import TestCase

from orange_datashare.light import LightApi
from orange_datashare_test.abstract_test_case import AbstractTestCase
from orange_datashare_test.fake_requests import mock_api_response, load_resource_file


class LightApiTest(TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()
        self.light = LightApi(self.client)

    def _test_state(self, color, expected_file):
        self.client.put.return_value = mock_api_response('/api/v2/users/-/commands/light/state',
                                                         OK,
                                                         None,
                                                         'light', 'state', 'PUT_response.json')
        expected_request = json.loads(load_resource_file('light', 'state', expected_file))
        self.light.set_sate('-', ['light-udi'], True, color)
        self.client.put.assert_called_with(self.client.put.return_value.url, data=None, json=expected_request)

    def test_set_state_by_rgb(self):
        self._test_state([1, 2, 3], 'PUT_rgb_request.json')

    def test_set_state_by_hsl(self):
        self._test_state([10.0, 0.5, 0.6], 'PUT_hsl_request.json')

    def test_set_state_by_hex(self):
        self._test_state("#FF5500", 'PUT_hex_request.json')
