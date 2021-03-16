import os
import argparse
import json

from datetime import datetime, timedelta
from src import SolarMan


def save_json(folder: str, data: json):
    global timestamp
    global date_start

    date_format = '%Y_%m_%d_%H%M%S'

    file_name = './data/{folder}/solarman_{date_start}_{timestamp}.json'.\
        format(
            folder=folder,
            date_start=date_start.strftime(date_format),
            timestamp=timestamp.strftime(date_format)
        )

    with open(
            file_name,
            mode='w',
            encoding='UTF-8') as f:
        json.dump(data, f)


parser = argparse.ArgumentParser(
    description='Downloads last 24 hour energy \
        generation data from SolarMan API')
parser.add_argument('--date_start',
                    action='store',
                    type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                    dest='date_start',
                    help='Start date of extraction (optional)- default now')
args = parser.parse_args()

timestamp = datetime.now()

# determine date start date
# if left empty, use current timestamp
date_start = args.date_start
date_start = date_start if date_start else timestamp

# calculate end date as last 24 hours
date_end = date_start - timedelta(hours=24)

# initialize new SolarMan instance
solarman = SolarMan.SolarMan(
    id=os.environ['ID'],
    secret=os.environ['SECRET_KEY']
)

solarman.get_token()  # access API

# uncomment if needed
# solarman.get_plants()  # gets available plants from user
# solarman.get_plants_devices()  # gets inverters

# download inverter data from given in .env file
data = solarman.get_inverter_data(
    inverter_id=os.environ['INVERTER_ID'],

    # in API date_end = date_end (reverse naming convention)
    timestamp_start=date_end,
    timestamp_end=date_start
)

# dump data
save_json('raw', data)
