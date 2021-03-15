import os
import argparse

from datetime import datetime, timedelta
from src import SolarMan

parser = argparse.ArgumentParser(
    description='Downloads last 24 hour energy \
        generation data from SolarMan API')
parser.add_argument('--date_start',
                    action='store',
                    type=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                    dest='date_start',
                    help='Start date of extraction (optional)- default now')
args = parser.parse_args()

# determine date start date
# if left empty, use current timestamp
date_start = args.date_start
date_start = date_start if date_start else datetime.now()

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
