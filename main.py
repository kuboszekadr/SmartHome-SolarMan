from os import environ
import yaml

from datetime import datetime, timedelta
from src import download_history
from src.streams import stream_to_disk

from dotenv import load_dotenv


def get_date() -> datetime:
    with open('.meta.yaml') as f:
        data = yaml.load_all(f, Loader=yaml.FullLoader)

    result = data.get('last_date', None)
    if result is not None:
        result = datetime.strptime(result, '%Y-%m-%d')
        result = result + timedelta(days=1)
    else:
        result = datetime.strptime(data['date_start'], '%Y-%m-%d')

    return result


load_dotenv()
date = get_date().strftime('%Y-%m-%d')

download_history(
    app_id=environ.get('app_id'),
    app_secret=environ.get('app_secret'),
    password=environ.get('password'),
    email=environ.get('email'),
    station_id=environ.get('stations_id'),
    date=date
)
