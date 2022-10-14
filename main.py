import os
import json

from dotenv import load_dotenv
from src.Account import Account
from src.Station import Station

from datetime import date

load_dotenv()

app_id = os.environ.get('app_id')
app_secret = os.environ.get('app_secret')
password = os.environ.get('password')
email = os.environ.get('email')

station_id = os.environ.get('station_id')

account = Account(app_id, app_secret, password, email)
account.get_token()

station = Station(station_id, account)
data = station.history()

with open('data/{}.json') as f:
    json.dump(data)