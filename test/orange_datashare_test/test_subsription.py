"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
import json
from unittest import TestCase

from orange_datashare.client import InvalidStatusCode
from orange_datashare.imported import OK, NOT_FOUND, NO_CONTENT, CREATED
from orange_datashare.subscription import SubscriptionApi, Origin
from orange_datashare_test.abstract_test_case import AbstractTestCase
from orange_datashare_test.fake_requests import mock_api_response, load_resource_file


class SubscriptionApiTest(TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()
        self.subscription = SubscriptionApi(self.client)

    def test_list_subscriptions(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/subscriptions',
                                                         OK,
                                                         None,
                                                         'subscriptions', 'GET_response.json')

        subscriptions = self.subscription.list_subscriptions('-')
        self.client.get.assert_called_with(self.client.get.return_value.url, params={}, headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(subscriptions)
        self.assertIsInstance(subscriptions, list)
        self.assertEqual(1, len(subscriptions))
        self.assertEqual("sub_for_user_12345_to_temperatures", subscriptions[0]["key"])

    def test_get_succeed(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/subscriptions/subscription-key',
                                                         OK,
                                                         None,
                                                         'subscriptions', 'GET_{id}_response.json')

        subscription = self.subscription.get_subscription('-', 'subscription-key')
        self.client.get.assert_called_with(self.client.get.return_value.url, params=None, headers=self.DEFAULT_HEADERS)
        self.assertIsNotNone(subscription)
        self.assertIsInstance(subscription, dict)
        self.assertEqual("sub_for_user_12345_to_temperatures", subscription["key"])

    def test_get_not_found(self):
        self.client.get.return_value = mock_api_response('/api/v2/users/-/data/subscriptions/subscription-key',
                                                         NOT_FOUND,
                                                         None)
        with self.assertRaises(InvalidStatusCode):
            self.subscription.get_subscription('-', 'subscription-key')

    def test_update_while_subscription_not_existing(self):
        self._test_update(CREATED)

    def test_update__while_subscription_existing(self):
        self._test_update(OK)

    def _test_update(self, status_returned):
        self.client.put.return_value = mock_api_response('/api/v2/users/-/subscriptions/subscription-key',
                                                         status_returned,
                                                         None,
                                                         'subscriptions', 'PUT_{key}_response.json')
        request = json.loads(load_resource_file('subscriptions', 'PUT_{key}_request.json'))
        self.subscription.set_subscription('-', 'subscription-key', '/indoor/air/temperature',
                                           url='https://myhost/notification/callback?from=liveobjects',
                                           origin=Origin.ANY,
                                           filter=dict(metadata=dict(device='carpetcorp:icarpet3@02:00:00:12:e8:d2')
                                                       )
                                           )
        self.client.put.assert_called_with(self.client.put.return_value.url, data=None, json=request,
                                           headers=self.DEFAULT_HEADERS)

    def test_remove_single(self):
        self.client.delete.return_value = mock_api_response('/api/v2/users/-/subscriptions/subscription-key',
                                                            NO_CONTENT,
                                                            None)

        self.subscription.remove_subscription('-', 'subscription-key')
        self.client.delete.assert_called_with(self.client.delete.return_value.url, headers=self.DEFAULT_HEADERS)

    def test_remove_all(self):
        self.client.delete.return_value = mock_api_response('/api/v2/users/-/subscriptions',
                                                            NO_CONTENT,
                                                            None)

        self.subscription.remove_all_subscriptions('-')
        self.client.delete.assert_called_with(self.client.delete.return_value.url, headers=self.DEFAULT_HEADERS)
