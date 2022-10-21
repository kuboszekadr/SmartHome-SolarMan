import os
import json

from datetime import datetime as dt
from datetime import date


def stream_to_disk(data, root: str, data_date: date):
    file_name = data_date.strftime('%Y-%m-%d')
    folder_name = data_date.strftime('%Y-%m')

    folder_path = os.path.join(root, folder_name)
    file_path = os.path.join(folder_path, f'{file_name}.json')

    os.makedirs(folder_path, exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f)


def stream_to_api(data):
    device_id = 1
    sensor_id = 1

    station_data_items = data['stationDataItems']
    readings = [0]*len(station_data_items)

    for idx, station_data_item in enumerate(station_data_items):
        value = station_data_item['generationPower']
        
        timestamp = station_data_item['dateTime']
        timestamp = dt.fromtimestamp(timestamp)
        
        reading = {
            'measure_id': 1,
            'value': value,
            'timestamp': timestamp
        }
        readings[idx] = reading

    payload = {
        'device_id': device_id,
        'sensor_id': sensor_id,
        'readings': readings
    }
    # TODO
    pass