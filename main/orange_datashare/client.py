from http.client import UNAUTHORIZED
import json
import logging
from oauth2_client.credentials_manager import CredentialManager, ServiceInformation

from orange_datashare.connection import ConnectionApi
from orange_datashare.data import DataApi
from orange_datashare.device import DeviceApi
from orange_datashare.light import LightApi
from orange_datashare.subscription import SubscriptionApi
from orange_datashare.thermostat import ThermostatApi

_logger = logging.getLogger(__name__)

class InvalidStatusCode(Exception):
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

    def __str__(self):
        if self.body is None:
            return '%d' % self.status_code
        elif type(self.body) == str:
            return '%d : %s' % (self.status_code, self.body)
        else:
            return '%d : %s' % (self.status_code, json.dumps(self.body))



class DatashareClient(CredentialManager):
    ENDPOINT = 'https://datashare.orange.com'

    PROXIES = None

    def __init__(self, client_id, client_secret, scopes, skip_ssl_verifications=False):
        super(DatashareClient, self).__init__(
            ServiceInformation(authorize_service='%s/oauth/authorize' % DatashareClient.ENDPOINT,
                               token_service='%s/oauth/token' % DatashareClient.ENDPOINT,
                               client_id=client_id,
                               client_secret=client_secret,
                               scopes=scopes,
                               skip_ssl_verifications=skip_ssl_verifications),
            self.PROXIES)
        self._connection = ConnectionApi(self)
        self._device = DeviceApi(self)
        self._data = DataApi(self)
        self._light = LightApi(self)
        self._subscription = SubscriptionApi(self)
        self._thermostat = ThermostatApi(self)

    @property
    def connection(self):
        return self._connection

    @property
    def device(self):
        return self._device

    @property
    def data(self):
        return self._data

    @property
    def light(self):
        return self._light

    @property
    def subscription(self):
        return self._subscription

    @property
    def thermostat(self):
        return self._thermostat

    @staticmethod
    def _is_token_expired(response):
        if response.status_code == UNAUTHORIZED:
            try:
                json_data = response.json()
                return json_data.get('error', '') == 'invalid_token'
            except:
                return False
        else:
            return False

    def _get(self, uri, params=None, **kwargs):
        _logger.debug('_get - %s - params=%s',  uri, params)
        return DatashareClient._check_response(
            self.get('%s%s' % (DatashareClient.ENDPOINT, uri), params=params, **kwargs)
        ).json()

    def _post(self, uri, data=None, json=None, **kwargs):
        _logger.debug('_post - %s - data=%s - json=%s', uri, data, json)
        return self.post('%s%s' % (DatashareClient.ENDPOINT, uri), data=data, json=json, **kwargs)

    def _put(self, uri, data=None, json=None, **kwargs):
        _logger.debug('_put - %s - data=%s - json=%s', uri, data, json)
        return self.put('%s%s' % (DatashareClient.ENDPOINT, uri), data=data, json=json, **kwargs)

    def _patch(self, uri, data=None, json=None, **kwargs):
        _logger.debug('_patch - %s - data=%s - json=%s', uri, data, json)
        return self.patch('%s%s' % (DatashareClient.ENDPOINT, uri), data=data, json=json, **kwargs)

    def _delete(self, uri, **kwargs):
        _logger.debug('_delete - %s', uri)
        return self.delete('%s%s' % (DatashareClient.ENDPOINT, uri), **kwargs)

    @staticmethod
    def _check_response(response, expected_status=None):
        if expected_status is None and int(response.status_code / 100) == 2 or \
                                expected_status is not None and int(response.status_code) == expected_status:
            return response
        else:
            try:
                body = response.json()
            except Exception:
                body = response.text
            raise InvalidStatusCode(response.status_code, body)
