import yaml
import logging

from os import environ
from sys import stdout

from datetime import datetime as dt, timedelta
from src.download_history import download_history
from src.streams import stream_to_disk

from dotenv import load_dotenv
from time import sleep


def download_day_data(date: dt) -> None:
    data = download_history(
        app_id=environ['app_id'],
        app_secret=environ['app_secret'],
        password=environ['password'],
        email=environ['email'],
        station_id=environ['station_id'],
        date=date
    )

    stream_to_disk(data, './data', date)


def update_meta_file(config: dict) -> None:
    with open('.meta.yaml', 'w', encoding='UTF-8') as f:
        config['last_date'] = date.strftime(date_format)
        yaml.dump(config, f)


load_dotenv()
with open('.meta.yaml', 'r') as f:
    meta = yaml.load(f, yaml.FullLoader)

date_format = meta['date_format']
date = dt.strptime(meta['last_date'], date_format)
today = dt.today().date()

logging.basicConfig(
    format="'%(asctime)s | %(name)s | %(message)s'",
    datefmt="%Y-%m-%d %H:%M:%S%z",
    filename=f'./logs/{today.strftime(date_format)}.log',
    level=logging.DEBUG
)
logging.getLogger().addHandler(logging.StreamHandler(stdout))

while True:
    logging.info(f"Downloading data for day: {date.strftime(date_format)}")
    download_day_data(date)

    if date.date() == today:
        break

    date += timedelta(days=1)
    sleep(5)

meta['last_date'] = date.strftime(date_format)
update_meta_file(meta)
