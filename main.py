from os import environ
import yaml

from datetime import datetime, timedelta
from src.download_history import download_history
from src.streams import stream_to_disk

from dotenv import load_dotenv


def get_date() -> datetime:
    with open('.meta.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    result = data.get('last_date', None)
    result = datetime.strptime(result, '%Y-%m-%d')
    result = result + timedelta(days=1)
    result = min(result, datetime.today())

    return result


def download_day_data(date: datetime) -> None:
    data = download_history(
        app_id=environ.get('app_id'),
        app_secret=environ.get('app_secret'),
        password=environ.get('password'),
        email=environ.get('email'),
        station_id=environ.get('station_id'),
        date=date
    )

    stream_to_disk(data, './data', date.strftime('%Y-%m-%d'))

    with open('.meta.yaml', 'w', encoding='UTF-8') as f:
        data = {}
        data['last_date'] = date.strftime('%Y-%m-%d')
        yaml.dump(data, f)


load_dotenv()
date = get_date()
today = date.today()

while date <= today:
    download_day_data(date)
