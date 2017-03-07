"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
from enum import Enum

from orange_datashare.imported import CREATED, NO_CONTENT, OK

from orange_datashare.abstract_api import AbstractApi


class Origin(Enum):
    ANY = "any"
    ANY_BUT_ME = "any_but_me"
    VENDOR_ONLY = "vendor_only"


class SubscriptionApi(AbstractApi):
    def list_subscriptions(self, user_id, **params):
        return self.client._get('/api/v2/users/%s/subscriptions' % user_id, params=params)

    def get_subscription(self, user_id, key):
        return self.client._get('/api/v2/users/%s/subscriptions/%s' % (user_id, key))

    def set_subscription(self, user_id, key, path, url, origin=Origin.ANY_BUT_ME, filter=None):
        subscription=dict(path=path, url=url, origin=origin.value)
        if filter is not None:
            subscription['filter'] = filter
        self.client._check_response(
            self.client._put('/api/v2/users/%s/subscriptions/%s' % (user_id, key), json=subscription),
            expected_status=(CREATED, OK,))

    def remove_all_subscriptions(self, user_id):
        self.client._check_response(
            self.client._delete('/api/v2/users/%s/subscriptions' % user_id),
            expected_status=(NO_CONTENT,))

    def remove_subscription(self, user_id, key):
        self.client._check_response(self.client._delete('/api/v2/users/%s/subscriptions/%s' % (user_id, key)),
                                    expected_status=(NO_CONTENT,))
