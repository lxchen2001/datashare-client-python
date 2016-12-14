from http.client import CREATED, NO_CONTENT

from orange_datashare.abstract_api import AbstractApi


class ConnectionApi(AbstractApi):
    def create_connection(self, user_id, connector_name, key):
        return self.client._check_response(
            self.client._post('/api/v2/users/%s/connections' % user_id,
                              json=dict(connectorName=connector_name, key=key)),
            CREATED).json()

    def get_connection(self, user_id, connection_id):
        return self.client._get('/api/v2/users/%s/connections/%s' % (user_id, connection_id))

    def list_connections(self, user_id, **params):
        return self.client._get('/api/v2/users/%s/connections' % user_id, params=params)

    def update_connection_status(self, user_id, connection_id, status, reason):
        return self.client._check_response(
            self.client._put('/api/v2/users/%s/connections/%s' % (user_id, connection_id),
                             json=dict(status=status, reason=reason))).json()

    def delete_connection(self, user_id, connection_id):
        self.client._check_response(
            self.client._delete('/api/v2/users/%s/connections/%s' % (user_id, connection_id)),
            NO_CONTENT)
