import json

from datetime import datetime as dt
from copy import deepcopy


class SolarManConverter:
    """
    Class providing easy convertion between SolarMan API and SmartHome
    """

    def __init__(self, data: dict):
        self._data = deepcopy(data)

        # TODO
        self._device_id = 1
        self._sensor_id = 2

        self._temp_measure_id = 1
        self._power_measure_id = 2

        # initialize empty converted data
        self._converted = {'device_id': self._device_id, 'data': {}}

    def convert(self):
        results = []
        for data in self._data['datas']:
            r = {}
            r['sensor_id'] = self._sensor_id

            r['readings'] = [{'measure_id': 5, 'value': data['today_energy']}]
            r['timestamp'] = dt.strptime(data['time'],
                                         '%Y-%m-%dT%H:%M:%SZ').\
                strftime('%Y%m%d %H%M%S')

            results.append(r)

        self._converted['data'] = results

        return self._converted
