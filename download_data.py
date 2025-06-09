import yaml
import logging
import os

from sys import stdout
from datetime import datetime as dt, timedelta
from src.download_history import download_history
from src.streams import stream_to_disk
from src.config import app_config
from time import sleep

checkpoint_file = os.path.join(app_config.checkpoint_folder_path, 'checkpoint.yaml')

def load_checkpoint() -> dict:
    if not os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'w', encoding='UTF-8') as f:
            start_date = dt.today() - timedelta(days=7)
            yaml.dump({'last_date': start_date.strftime(app_config.date_format)}, f)

    with open(checkpoint_file, 'r') as f:
        checkpoint = yaml.safe_load(f)
    return checkpoint

def download_day_data(date: dt) -> None:
    """Download solar data for a specific date using configured credentials."""
    data = download_history(
        app_id=app_config.APP_ID,
        app_secret=app_config.APP_SECRET,
        password=app_config.PASSWORD,
        email=app_config.EMAIL,
        station_id=app_config.STATION_ID,
        date=date
    )

    stream_to_disk(data, os.path.join(app_config.storage_path), date)


def update_checkpoint_file(date: dt) -> None:
    """Update the checkpoint file with the latest processed date."""
    with open(checkpoint_file, 'r') as f:
        checkpoint = yaml.safe_load(f)

    checkpoint['last_date'] = date.strftime(app_config.date_format)

    with open(checkpoint_file, 'w', encoding='UTF-8') as f:
        yaml.dump(checkpoint, f)


def main():
    

    today = dt.today().date()
    log_file = os.path.join(app_config.logs_path, f'{today.strftime(app_config.date_format)}.log')
    logging.basicConfig(
        format="'%(asctime)s | %(name)s | %(message)s'",
        datefmt="%Y-%m-%d %H:%M:%S%z",
        filename=log_file,
        level=logging.DEBUG
    )
    logging.getLogger().addHandler(logging.StreamHandler(stdout))

    checkpoint = load_checkpoint()
    date = dt.strptime(checkpoint['last_date'], app_config.date_format)

    while True:
        logging.info(f"Downloading data for day: {date.strftime(app_config.date_format)}")

        try:
            download_day_data(date)
        except Exception as e:
            logging.error(f"Unhandled error {e}: {repr(e)}")
            raise e
        else:
            update_checkpoint_file(date)

        if date.date() >= today:
            break

        date += timedelta(days=1)
        sleep(5)


if __name__ == "__main__":
    main()
