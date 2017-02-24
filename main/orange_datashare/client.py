"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""

import json
import logging

from oauth2_client.credentials_manager import CredentialManager, ServiceInformation

from orange_datashare.command import CommandApi
from orange_datashare.connection import ConnectionApi
from orange_datashare.data import DataApi, DataApiV1
from orange_datashare.device import DeviceApi
from orange_datashare.imported import UNAUTHORIZED
from orange_datashare.subscription import SubscriptionApi

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
            ServiceInformation(authorize_service='%s/oauth/authorize' % self.ENDPOINT,
                               token_service='%s/oauth/token' % self.ENDPOINT,
                               client_id=client_id,
                               client_secret=client_secret,
                               scopes=scopes,
                               skip_ssl_verifications=skip_ssl_verifications),
            self.PROXIES)
        self._connection = ConnectionApi(self)
        self._device = DeviceApi(self)
        self._data = DataApi(self)
        self._deprecated_data = DataApiV1(self)
        self._subscription = SubscriptionApi(self)
        self._command = CommandApi(self)

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
    def deprecated_data(self):
        return self._deprecated_data

    @property
    def subscription(self):
        return self._subscription

    @property
    def command(self):
        return self._command

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
        _logger.debug('_get - %s - params=%s', uri, params)
        return DatashareClient._check_response(
            self.get('%s%s' % (self.ENDPOINT, uri), params=params, **self._add_encoding(**kwargs))
        ).json()

    def _post(self, uri, data=None, json=None, **kwargs):
        _logger.debug('_post - %s - data=%s - json=%s', uri, data, json)
        return self.post('%s%s' % (self.ENDPOINT, uri), data=data, json=json, **self._add_encoding(**kwargs))

    def _put(self, uri, data=None, json=None, **kwargs):
        _logger.debug('_put - %s - data=%s - json=%s', uri, data, json)
        return self.put('%s%s' % (self.ENDPOINT, uri), data=data, json=json, **self._add_encoding(**kwargs))

    def _patch(self, uri, data=None, json=None, **kwargs):
        _logger.debug('_patch - %s - data=%s - json=%s', uri, data, json)
        return self.patch('%s%s' % (self.ENDPOINT, uri), data=data, json=json, **self._add_encoding(**kwargs))

    def _delete(self, uri, **kwargs):
        _logger.debug('_delete - %s', uri)
        return self.delete('%s%s' % (self.ENDPOINT, uri), **self._add_encoding(**kwargs))

    @staticmethod
    def _add_encoding(**kwargs):
        headers = kwargs.get('headers', None)
        if headers is None:
            headers = dict()
            kwargs['headers'] = headers
        headers['Accept'] = 'application/json'
        return kwargs

    @staticmethod
    def _check_response(response, expected_status=None):
        if expected_status is None and int(response.status_code / 100) == 2 or \
                                expected_status is not None and int(response.status_code) == expected_status:
            return response
        else:
            try:
                body = response.json()
            except BaseException as ex:
                _logger.warning('_check_response - response body is not json: %s - %s', type(ex), str(ex),
                                exc_info=True)
                body = response.text
            raise InvalidStatusCode(response.status_code, body)
