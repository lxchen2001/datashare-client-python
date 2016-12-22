from datetime import datetime
from enum import Enum

from orange_datashare.abstract_api import AbstractApi


class ThermostatMode(Enum):
    ANTIFREEZE = "antifreeze"
    PROGRAM = "program"
    ENERGYSAVER = "energysaver"
    MANUAL = "manual"


class ThermostatApi(AbstractApi):
    def set_mode(self, user_id, thermostat_udis, mode, temperature, end_date):
        if end_date is not None and isinstance(end_date, int) or isinstance(end_date, float):
            end_date = '%s.%03dZ' % (datetime.fromtimestamp(int(end_date)).strftime('%Y-%m-%dT%H:%M:%S'),
                                     int((end_date * 1000) % 1000))
        request = dict(params=dict(endDate=end_date, temperature=temperature, type=mode.value),
                       target=dict(byUdi=thermostat_udis))
        return self.client._put('/api/v2/users/%s/commands/thermostat/mode' % user_id, json=request)
