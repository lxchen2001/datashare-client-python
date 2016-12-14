from orange_datashare.abstract_api import AbstractApi


class SubscriptionApi(AbstractApi):
    def list_subscriptions(self, user_id, **params):
        return self.client._get('/api/v2/users/%s/subscriptions' % user_id, params=params)

    def get_subscription(self, user_id, key):
        return self.client._get('/api/v2/users/%s/subscriptions/%s' % (user_id, key))

    def update_subscriptions(self, user_id, key, data):
        return self.client._put('/api/v2/users/%s/subscriptions/%s' % (user_id, key), json=data)

    def remove_subscriptions(self, user_id):
        return self.client._delete('/api/v2/users/%s/subscriptions' % user_id)

    def remove_subscription(self, user_id, key):
        return self.client._delete('/api/v2/users/%s/subscriptions/%s' % (user_id, key))
