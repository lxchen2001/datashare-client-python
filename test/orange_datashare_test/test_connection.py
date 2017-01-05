"""
Copyright (C) 2016 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
from orange_datashare.imported import OK, NOT_FOUND, NO_CONTENT
from unittest import TestCase

from orange_datashare.client import InvalidStatusCode
from orange_datashare.connection import ConnectionApi
from orange_datashare_test.abstract_test_case import AbstractTestCase
from orange_datashare_test.fake_requests import mock_api_response


class ConnectionApiTest(TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()
        self.connections = ConnectionApi(self.client)

    def test_list(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/connections',
                                                         OK,
                                                         None,
                                                         'connections', 'GET_response.json')

        connections = self.connections.list_connections('-')
        self.client.get.assert_called_with(self.client.get.return_value.url, params={})
        self.assertIsNotNone(connections)
        self.assertIsInstance(connections, list)
        self.assertEqual(1, len(connections))
        self.assertIsInstance(connections[0], dict)
        self.assertEqual("carpetcorp", connections[0]["connectorName"])
        self.assertEqual("NONE", connections[0]["error"])

    def test_get_succeed(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/connections/connection-id',
                                                         OK,
                                                         None,
                                                         'connections', 'GET_{id}_response.json')

        connection = self.connections.get_connection('-', 'connection-id')
        self.client.get.assert_called_with(self.client.get.return_value.url, params=None)
        self.assertIsNotNone(connection)
        self.assertIsInstance(connection, dict)
        self.assertEqual("carpetcorp", connection["connectorName"])
        self.assertEqual("NONE", connection["error"])

    def test_get_not_found(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/connections/connection-id',
                                                         NOT_FOUND,
                                                         None)
        with self.assertRaises(InvalidStatusCode):
            self.connections.get_connection('-', 'connection-id')

    def test_create(self):
        self.client.post.return_value = mock_api_response(
            '/api/v2/users/-/connections',
            OK,
            None,
            'connections', 'POST_response.json')
        connection = self.connections.create_connection('-', 'test-connector', 'test-key')
        self.client.post.assert_called_with(self.client.post.return_value.url,
                                            data=None,
                                            json=dict(connectorName='test-connector', key='test-key'))
        self.assertIsNotNone(connection)
        self.assertIsInstance(connection, dict)
        self.assertEqual("test-connector", connection["connectorName"])
        self.assertEqual("test-key", connection["key"])

    def test_delete(self):
        self.client.delete.return_value = mock_api_response('/api/v2/users/-/connections/connection-id',
                                                            NO_CONTENT,
                                                            None)

        self.connections.delete_connection('-', 'connection-id')
        self.client.delete.assert_called_with(self.client.delete.return_value.url)

    def test_update(self):
        self.client.put.return_value = mock_api_response('/api/v2/users/-/connections/connection-id',
                                                         OK,
                                                         None,
                                                         'connections', 'PUT_{id}_response.json')

        connection = self.connections.update_connection_status('-', 'connection-id', 'WORKING', 'NONE')
        self.assertIsNotNone(connection)
        self.assertIsInstance(connection, dict)
        self.assertEqual("carpetcorp", connection["connectorName"])
        self.assertEqual("NONE", connection["error"])
        self.client.put.assert_called_with(self.client.put.return_value.url,
                                           data=None,
                                           json=dict(status='WORKING', reason='NONE'))
