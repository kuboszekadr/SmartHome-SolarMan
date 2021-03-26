import json

from datetime import datetime as dt
from copy import deepcopy


class SolarManConverter:
    """
    Class providing easy convertion between SolarMan API and SmartHome
    """

    def __init__(self,
                 device_id: int,
                 device_sensor_id: int,
                 power_measure_id: int
                 ):

        self._device_id = device_id
        self._sensor_id = device_sensor_id

        self._power_measure_id = power_measure_id

        # initialize empty converted data
        self._converted = {'device_id': self._device_id, 'data': {}}

    def convert_inverter_daily_data(self, data):
        """
        Converts data from SolarMAN-API inverter cumulated daily
        data to SmartHome-API format

        @returns: converted data (cumulated daily inverter data)
        """
        results = []

        # loop through avaiable data
        for entry in data['datas']:
            r = {}  # place holder for dict data

            r['sensor_id'] = self._sensor_id
            r['readings'] = [
                {'measure_id': self._power_measure_id,
                 'value': entry['today_energy']
                 }]

            # create timestamp data, convert to SmartHome
            r['timestamp'] = dt.strptime(entry['time'], '%Y-%m-%dT%H:%M:%SZ')
            r['timestamp'] = r['timestamp'].strftime('%Y%m%d %H%M%S')

            results.append(r)

        self._converted['data'] = results

        return self._converted
