"""
Copyright (C) 2016 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
import json
import logging
import os
import random
import stat
import sys

from oauth2_client.credentials_manager import OAuthError

from orange_datashare.client import DatashareClient

_configuration_directory = os.path.join(os.path.expanduser('~'), '.datashare-client')
_configuration_file = os.path.join(_configuration_directory, 'configuration.json')

_logger = logging.getLogger(__name__)


class _CommandClient(DatashareClient):
    def __init__(self, target, client_id, client_secret, scopes, skip_ssl_verification):
        self.PROXIES = dict(http=os.environ.get('http_proxy', ''), https=os.environ.get('https_proxy', ''))
        super(_CommandClient, self).__init__(client_id, client_secret, scopes, skip_ssl_verification)
        self.ENDPOINT = target

    def set_tokens(self, access_token, refresh_token):
        self.refresh_token = refresh_token
        self._init_session()
        self._set_access_token(access_token)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == OAuthError:
            _logger.error('OAuth error. Configuration will be erased')
            os.remove(_configuration_file)
        else:
            self.save_configuration()

    def save_configuration(self):
        try:
            with open(_configuration_file, 'r') as f:
                existing_configuration = json.load(f)
                if type(existing_configuration) is not dict:
                    existing_configuration = dict()
        except:
            existing_configuration = dict()
        with open(_configuration_file, 'w') as f:
            access_token = None
            if self._session is not None:
                authorization = self._session.headers.get('Authorization')
                if authorization is not None:
                    access_token = authorization[len('Bearer '):]
            configuration = dict(client_id=self.service_information.client_id,
                                 client_secret=self.service_information.client_secret,
                                 scopes=self.service_information.scopes,
                                 skip_ssl_verifications=self.service_information.skip_ssl_verifications)
            if self.refresh_token is not None:
                configuration['refresh_token'] = self.refresh_token
            if access_token is not None:
                configuration['access_token'] = access_token
            existing_configuration[self.ENDPOINT] = configuration
            json.dump(existing_configuration, f, indent=1)


def _prompt(msg):
    sys.stdout.write('%s: ' % msg)
    sys.stdout.flush()
    response = sys.stdin.readline()
    return response.rstrip('\r\n')


def _init_oauth_process(client):
    default_redirect_uri = 'http://localhost:8080'
    redirect_uri = _prompt('Redirect uri: [%s]' % default_redirect_uri)
    if len(redirect_uri) == 0:
        redirect_uri = default_redirect_uri
    url_to_open = client.init_authorize_code_process(redirect_uri, state=str(random.random()))
    _logger.warning('***** OPEN THIS URL IN YOUR BROWSER *****\n\t%s', url_to_open)
    code = client.wait_and_terminate_authorize_code_process()
    client.init_with_authorize_code(redirect_uri=redirect_uri, code=code)


def _init_client(target):
    global _configuration_directory

    client_id = _prompt('Client Id')
    client_secret = _prompt('Client Secret')
    scopes = _prompt('Scopes').split(' ')

    skip_ssl_verification = _prompt('Skip ssl verification <no/yes> [no]').lower() == 'yes'
    if not os.path.exists(_configuration_directory):
        os.mkdir(_configuration_directory, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    client = _CommandClient(target, client_id, client_secret, scopes, skip_ssl_verification)
    _init_oauth_process(client)
    # save first time, meaning configuration works
    client.save_configuration()
    return client


def load_client(target):
    global _configuration_file
    try:
        with open(_configuration_file, 'r') as f:
            configurations = json.load(f)
            if type(configurations) is not dict or target not in configurations:
                return _init_client(target)
            configuration = configurations[target]
            client_id = configuration.get('client_id')
            client_secret = configuration.get('client_secret')
            scopes = configuration.get('scopes')
            skip_ssl_verifications = configuration.get('skip_ssl_verifications', False)
            access_token = configuration.get('access_token')
            refresh_token = configuration.get('refresh_token')
            if client_id is None or client_secret is None or scopes is None:
                return _init_client(target)
            result = _CommandClient(target, client_id, client_secret, scopes, skip_ssl_verifications)
            if refresh_token is not None:
                # do not accept access without refresh token
                if access_token is not None:
                    result.set_tokens(access_token, refresh_token)
                else:
                    result.init_with_token(refresh_token)
            else:
                _init_oauth_process(result)
            return result
    except IOError:
        return _init_client(target)
