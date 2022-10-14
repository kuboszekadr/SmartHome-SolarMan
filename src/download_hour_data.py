from Endpoints.Account import Account
from Endpoints.Station import Station

import json
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--app_id')
parser.add_argument('--app_secret')
parser.add_argument('--password')
parser.add_argument('--email')
parser.add_argument('--station_id')
parser.add_argument('--output_path')

args = parser.parse_args()
account = Account(args.app_id, args.app_secret, args.password, args.email)
account.get_token()

station = Station(args.station_id, account)
data = station.history()

file_path = os.path.join(args.output_path, 'TODO.json')

with open(file_path) as f:
    json.dump(data)