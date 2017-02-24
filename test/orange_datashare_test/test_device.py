"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
import json
from orange_datashare.imported import OK, NOT_FOUND
from unittest import TestCase

from orange_datashare.client import InvalidStatusCode
from orange_datashare.device import DeviceApi
from orange_datashare_test.abstract_test_case import AbstractTestCase
from orange_datashare_test.fake_requests import mock_api_response, load_resource_file


class DeviceApiTest(TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()
        self.devices = DeviceApi(self.client)

    def test_list(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/connections/connection-id/devices',
                                                         OK,
                                                         None,
                                                         'devices', 'GET_response.json')

        devices = self.devices.list_devices('-', 'connection-id')
        self.client.get.assert_called_with(self.client.get.return_value.url, params={}, headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(devices)
        self.assertIsInstance(devices, list)
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], dict)
        self.assertEqual("carpetcorp:icarpet3@02:00:00:12:e8:d2", devices[0]["udi"])
        self.assertEqual("NONE", devices[0]["error"])

    def test_get_succeed(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/connections/connection-id/devices/device-id',
                                                         OK,
                                                         None,
                                                         'devices', 'GET_{id}_response.json')

        device = self.devices.get_device('-', 'connection-id', 'device-id')
        self.client.get.assert_called_with(self.client.get.return_value.url, params=None, headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(device)
        self.assertIsInstance(device, dict)
        self.assertEqual("carpetcorp:icarpet3@02:00:00:12:e8:d2", device["udi"])
        self.assertEqual("NONE", device["error"])

    def test_get_not_found(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/connections/connection-id/devices/device-id',
                                                         NOT_FOUND,
                                                         None)
        with self.assertRaises(InvalidStatusCode):
            self.devices.get_device('-', 'connection-id', 'device-id')

    def test_set_connection_devices(self):
        self.client.put.return_value = mock_api_response('/api/v2/users/-/connections/connection-id/devices',
                                                         OK,
                                                         None,
                                                         'devices', 'PUT_response.json')
        request = json.loads(load_resource_file('devices', 'PUT_request.json'))
        devices = self.devices.set_connection_devices('-', 'connection-id',
                                                      devices=request)
        self.client.put.assert_called_with(self.client.put.return_value.url,
                                           data=None,
                                           json=request,
                                           headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(devices)
        self.assertIsInstance(devices, list)
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], dict)
        self.assertEqual("connection:model:instance", devices[0]["udi"])
        self.assertEqual("NONE", devices[0]["error"])
        self.assertIsNone(devices[0]["parentId"])

    def test_update_connection_devices(self):
        self.client.patch.return_value = mock_api_response('/api/v2/users/-/connections/connection-id/devices',
                                                           OK,
                                                           None,
                                                           'devices', 'PATCH_response.json')
        request = json.loads(load_resource_file('devices', 'PATCH_request.json'))
        devices = self.devices.update_connection_devices('-', 'connection-id',
                                                         devices=request)
        self.client.patch.assert_called_with(self.client.patch.return_value.url,
                                             data=None,
                                             json=request,
                                             headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(devices)
        self.assertIsInstance(devices, list)
        self.assertEqual(2, len(devices))
        self.assertIsInstance(devices[0], dict)
        self.assertEqual("connection:model:instance", devices[0]["udi"])
        self.assertIsNone(devices[0]["parentId"])
        self.assertEqual("connection:child:instance-child", devices[1]["udi"])
        self.assertEqual(devices[0]["id"], devices[1]["parentId"])
