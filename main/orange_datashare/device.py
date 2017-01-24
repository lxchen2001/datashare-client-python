"""
Copyright (C) 2016-2017 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution
"""
from orange_datashare.abstract_api import AbstractApi


class DeviceApi(AbstractApi):
    def list_devices(self, user_id, connection_id, **params):
        return self.client._get('/api/v2/users/%s/connections/%s/devices' % (user_id, connection_id), params=params)

    def get_device(self, user_id, connection_id, device_id):
        return self.client._get('/api/v2/users/%s/connections/%s/devices/%s' % (user_id, connection_id, device_id))

    def update_connection_devices(self, user_id, connection_id, devices):
        return self.client._check_response(
            self.client._patch('/api/v2/users/%s/connections/%s/devices' % (user_id, connection_id), json=devices)
        ).json()

    def set_connection_devices(self, user_id, connection_id, devices):
        return self.client._check_response(
            self.client._put('/api/v2/users/%s/connections/%s/devices' % (user_id, connection_id), json=devices)
        ).json()
