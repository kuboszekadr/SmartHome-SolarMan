from datetime import datetime as dt
from dataclasses import dataclass

import requests


@dataclass
class DataCollectorStreaming:
    device_name: str
    url: str
    port: int

    @property
    def endpoint(self) -> str:
        result = f"http://{self.url}:{self.port}/api/v2.0/data_collector"
        return result

    def stream(self, data):
        station_data_items = data['stationDataItems']
        readings = [0]*len(station_data_items)

        if len(readings) == 0:
            return

        for idx, station_data_item in enumerate(station_data_items):
            value = station_data_item['generationPower']

            timestamp = station_data_item['dateTime']
            timestamp = dt.fromtimestamp(timestamp)

            reading = {
                'measure_name': "power",
                'value': value,
                'timestamp': timestamp.strftime('%Y%m%d %H%M%S')
            }
            readings[idx] = reading

        payload = {
            'device_name': self.device_name,
            'readings': readings
        }

        requests.post(
            url=self.endpoint,
            json=payload
        )
