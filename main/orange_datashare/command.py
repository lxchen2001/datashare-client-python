"""
Copyright (C) 2016 Orange
This software is distributed under the terms and conditions of the 'BSD 3'
license which can be found in the file 'LICENSE' in this package distribution 
"""
from datetime import datetime
from enum import Enum

from orange_datashare.abstract_api import AbstractApi
from orange_datashare.imported import ACCEPTED


class ThermostatMode(Enum):
    ANTIFREEZE = "antifreeze"
    PROGRAM = "program"
    ENERGYSAVER = "energysaver"
    MANUAL = "manual"


class CommandApi(AbstractApi):
    def set_light_state(self, user_id, light_udis, on, color=None):
        request = dict(params=dict(on=on), target=dict(byUdi=light_udis))
        if color is not None:
            if isinstance(color, str):
                request["params"]["color"] = dict(hex=color)
            elif isinstance(color, tuple) or isinstance(color, list):
                if len(color) != 3:
                    raise ValueError(
                        'color must either be a a string for hew representation , a 3-tuple int for RGB or a 3-tuple float for HLS')
                if isinstance(color[0], int) and isinstance(color[1], int) and isinstance(color[2], int):
                    request["params"]["color"] = dict(rgb=color)
                else:
                    request["params"]["color"] = dict(hsl=color)
        return self.client._check_response(
            self.client._put('/api/v2/users/%s/commands/light/state' % user_id,
                             json=request),
            expected_status=ACCEPTED
        ).json()

    def set_thermostat_mode(self, user_id, thermostat_udis, mode, temperature, end_date):
        if end_date is not None and isinstance(end_date, int) or isinstance(end_date, float):
            end_date = '%s.%03dZ' % (datetime.fromtimestamp(int(end_date)).strftime('%Y-%m-%dT%H:%M:%S'),
                                     int((end_date * 1000) % 1000))
        request = dict(params=dict(endDate=end_date, temperature=temperature, type=mode.value),
                       target=dict(byUdi=thermostat_udis))
        return self.client._check_response(
            self.client._put('/api/v2/users/%s/commands/thermostat/mode' % user_id, json=request),
            expected_status=ACCEPTED
        ).json()
