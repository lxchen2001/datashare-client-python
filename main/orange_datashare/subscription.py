from http.client import CREATED, NO_CONTENT
from orange_datashare.abstract_api import AbstractApi


class SubscriptionApi(AbstractApi):
    def list_subscriptions(self, user_id, **params):
        return self.client._get('/api/v2/users/%s/subscriptions' % user_id, params=params)

    def get_subscription(self, user_id, key):
        return self.client._get('/api/v2/users/%s/subscriptions/%s' % (user_id, key))

    def set_subscription(self, user_id, key, data):
        self.client._check_response(
            self.client._put('/api/v2/users/%s/subscriptions/%s' % (user_id, key), json=data),
            expected_status=CREATED)

    def remove_subscriptions(self, user_id):
        self.client._check_response(
            self.client._delete('/api/v2/users/%s/subscriptions' % user_id),
            expected_status=NO_CONTENT)

    def remove_subscription(self, user_id, key):
        self.client._check_response(self.client._delete('/api/v2/users/%s/subscriptions/%s' % (user_id, key)),
                                    expected_status=NO_CONTENT)
