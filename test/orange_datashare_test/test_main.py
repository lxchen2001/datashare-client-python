"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
import sys
import unittest
from orange_datashare_test import mock

import orange_datashare.main as main
from orange_datashare.data import StatsField
from orange_datashare.data import BoundariesSearchOption
from orange_datashare.subscription import Origin
from orange_datashare.command import ThermostatMode


class TestMain(unittest.TestCase):
    @mock.patch.object(sys, 'argv', ['main', 'list_connections'])
    @mock.patch('orange_datashare.main.load_client')
    def test_list_connections(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.connection.list_connections.assert_called_with('me')

    @mock.patch.object(sys, 'argv', ['main', 'get_connection', '666'])
    @mock.patch('orange_datashare.main.load_client')
    def test_get_connection(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.connection.get_connection.assert_called_with('me', 666)

    @mock.patch.object(sys, 'argv', ['main', 'delete_connection', '666'])
    @mock.patch('orange_datashare.main.load_client')
    def test_delete_connection(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.connection.delete_connection.assert_called_with('me', 666)

    @mock.patch.object(sys, 'argv', ['main', 'create_connection', 'name', 'key'])
    @mock.patch('orange_datashare.main.load_client')
    def test_create_connection(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.connection.create_connection.assert_called_with('me', 'name', 'key')

    @mock.patch.object(sys, 'argv', ['main', 'update_connection_status', '666', 'ERROR', 'STORAGE'])
    @mock.patch('orange_datashare.main.load_client')
    def test_update_connection_status(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.connection.update_connection_status.assert_called_with('me', 666, 'ERROR', 'STORAGE')

    @mock.patch.object(sys, 'argv', ['main', 'list_devices', '666'])
    @mock.patch('orange_datashare.main.load_client')
    def test_list_devices(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.device.list_devices.assert_called_with('me', 666)

    @mock.patch.object(sys, 'argv', ['main', 'get_device', '666', '777'])
    @mock.patch('orange_datashare.main.load_client')
    def test_get_device(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.device.get_device.assert_called_with('me', 666, 777)

    @mock.patch.object(sys, 'argv', ['main', 'set_devices', '666', '{"key": "value"}'])
    @mock.patch('orange_datashare.main.load_client')
    def test_set_device(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.device.set_connection_devices.assert_called_with('me', 666, dict(key="value"))

    @mock.patch.object(sys, 'argv', ['main', 'update_devices', '666', '{"key": "value"}'])
    @mock.patch('orange_datashare.main.load_client')
    def test_update_device(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.device.update_connection_devices.assert_called_with('me', 666, dict(key="value"))

    @mock.patch.object(sys, 'argv', ['main', 'list_subscriptions'])
    @mock.patch('orange_datashare.main.load_client')
    def test_list_subscriptions(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.subscription.list_subscriptions.assert_called_with('me')

    @mock.patch.object(sys, 'argv', ['main', 'get_subscription', 'key'])
    @mock.patch('orange_datashare.main.load_client')
    def test_get_subscription(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.subscription.get_subscription.assert_called_with('me', 'key')

    @mock.patch.object(sys, 'argv', ['main', 'set_subscription', 'key', '/indoor/air/temperature',
                                     'http://somewhere-over-the-rainbow', 'any', '{"key": "value"}'])
    @mock.patch('orange_datashare.main.load_client')
    def test_set_subscription(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.subscription.set_subscription.assert_called_with('me', 'key', '/indoor/air/temperature',
                                                                     'http://somewhere-over-the-rainbow',
                                                                     Origin.ANY, dict(key="value"))

    @mock.patch.object(sys, 'argv', ['main', 'remove_subscription', 'key'])
    @mock.patch('orange_datashare.main.load_client')
    def test_remove_subscription(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.subscription.remove_subscription.assert_called_with('me', 'key')

    @mock.patch.object(sys, 'argv', ['main', 'remove_all_subscriptions'])
    @mock.patch('orange_datashare.main.load_client')
    def test_remove_subscriptions(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.subscription.remove_subscriptions.assert_called_with('me')

    @mock.patch.object(sys, 'argv', ['main', 'list_streams'])
    @mock.patch('orange_datashare.main.load_client')
    def test_list_streams(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.data.list_streams.assert_called_with('me')

    @mock.patch.object(sys, 'argv', ['main', 'get_data', '/indoor/air/temperature'])
    @mock.patch('orange_datashare.main.load_client')
    def test_get_data(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.data.get_data.assert_called_with('me', '/indoor/air/temperature')

    @mock.patch.object(sys, 'argv', ['main', 'write_data', '/indoor/air/temperature', '{"key": "value"}'])
    @mock.patch('orange_datashare.main.load_client')
    def test_write_data(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.data.write_data.assert_called_with('me', '/indoor/air/temperature', dict(key="value"))

    @mock.patch.object(sys, 'argv', ['main', 'get_stats', '/indoor/air/temperature'])
    @mock.patch('orange_datashare.main.load_client')
    def test_get_all_stats(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.data.get_stats.assert_called_with('me', '/indoor/air/temperature', [])

    @mock.patch.object(sys, 'argv', ['main', 'get_stats', '/indoor/air/temperature', 'min', 'max', 'avg'])
    @mock.patch('orange_datashare.main.load_client')
    def test_get_specific_stats(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.data.get_stats.assert_called_with('me', '/indoor/air/temperature',
                                                      [StatsField.MIN, StatsField.MAX, StatsField.AVG])

    @mock.patch.object(sys, 'argv', ['main', 'get_summaries', '/me/sleep'])
    @mock.patch('orange_datashare.main.load_client')
    def test_get_summary(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.data.get_summaries.assert_called_with('me', '/me/sleep')

    @mock.patch.object(sys, 'argv', ['main', 'get_boundaries', 'both', '/me/sleep', '/indoor/air/temperature'])
    @mock.patch('orange_datashare.main.load_client')
    def test_get_boundaries(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.data.get_boundaries.assert_called_with('me', BoundariesSearchOption.BOTH, ['/me/sleep', '/indoor/air/temperature'])

    @mock.patch.object(sys, 'argv', ['main', 'set_light_state', 'light-udi', 'on', "#FFDDEE"])
    @mock.patch('orange_datashare.main.load_client')
    def test_set_light_state(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.command.set_light_state.assert_called_with('me', ['light-udi'], True, "#FFDDEE")

    @mock.patch.object(sys, 'argv', ['main', 'set_plug_state', 'plug-udi', 'on'])
    @mock.patch('orange_datashare.main.load_client')
    def test_set_plug_state(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.command.set_plug_state.assert_called_with('me', ['plug-udi'], True)

    @mock.patch.object(sys, 'argv', ['main', 'set_light_state', 'light-udi-1,light-udi-2', 'on'])
    @mock.patch('orange_datashare.main.load_client')
    def test_set_light_state_without_color(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.command.set_light_state.assert_called_with('me', ['light-udi-1', 'light-udi-2'], True, None)

    @mock.patch.object(sys, 'argv', ['main', 'set_thermostat_mode', 'thermostat-udi-1,thermostat-udi-2',
                                     'antifreeze', '29.3', "2016-12-21T11:35:11.745Z"])
    @mock.patch('orange_datashare.main.load_client')
    def test_set_thermostat_mode(self, mock_client_loader):
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
        fake_client.command.set_thermostat_mode.assert_called_with('me', ['thermostat-udi-1','thermostat-udi-2'],
                                                                   ThermostatMode.ANTIFREEZE, 29.3,
                                                                   "2016-12-21T11:35:11.745Z")

    @staticmethod
    def _configure_mock_client(mock_client_loader):
        fake_client = mock_client_loader()
        fake_client.__enter__.return_value = fake_client
        return fake_client
        fake_client = self._configure_mock_client(mock_client_loader)
        main.main()
