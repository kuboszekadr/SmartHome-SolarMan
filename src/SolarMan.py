import requests
import json
import datetime


class SolarMan:
    BASE_URL = 'https://openapi.solarmanpv.com/v1'
    DT_ISO8601 = '%Y-%m-%d %H:%M:%S'

    def __init__(self, id, secret):
        self._id = id
        self._secret = secret
        self._auth_header = {'token': None, 'uid': 0}
        self._refresh_token = ''
        self._expires_id = 0
        self._plants_id = []
        self._devices = {}

    def get_token(self):
        """
        Gets access token from SolarMAN API
        """
        url = SolarMan.BASE_URL + '/oauth2/accessToken'
        params = {
            'client_id': self._id,
            'client_secret': self._secret,
            'grant_type': 'client_credentials'
        }

        r = requests.get(url, params).json()

        self._auth_header['uid'] = r['data']['uid']
        self._auth_header['token'] = r['data']['access_token']

    def get_plants(self) -> None:
        """
        Downloads plant list from SolarMan API
        """
        url = SolarMan.BASE_URL + '/plant/list'

        r = requests.get(url, headers=self._auth_header).json()

        plants = r['data']['plants']
        for plant in plants:
            self._plants_id.append(plant['plant_id'])

    def get_plants_devices(self) -> None:
        """
        Downloads devices from avaiable plants
        """
        url = SolarMan.BASE_URL + '/device/list'

        for plant_id in self._plants_id:
            r = requests.get(
                url,
                params={'plant_id': plant_id},
                headers=self._auth_header
            )

            r = r.json()
            devices = [x['device_id'] for x in r['data']['devices']]
            self._devices[plant_id] = devices

    def get_plant_power_data(self, plant_id: int, date: datetime.datetime):
        url = SolarMan.BASE_URL + '/plant/power'

        params = {
            'plant_id': plant_id,
            'date': date.strftime(),
            # 'use_dst': 'false'  # ignore summer/winter time
        }

        r = requests.get(
            url,
            params=params,
            headers=self._auth_header
        ).json()

        return r['data']

    def get_inverter_data(
        self,
        inverter_id: int,
        timestamp_start: datetime.datetime,
        timestamp_end: datetime.datetime
    ) -> dict:
        """
        Downloads data from the inverter

        @param inverter_id: inverter id to get energy data
        @param timestamp_start: starting point for the data
        @param timestamp_end: ending point for the data

        @returns dict with API response
        """

        url = SolarMan.BASE_URL + '/device/inverter/data'
        params = {
            'device_id': inverter_id,
            'start_date': timestamp_start.strftime(SolarMan.DT_ISO8601),
            'end_date': timestamp_end.strftime(SolarMan.DT_ISO8601),
            'perpage': 1000,
            'use_dst': 'false'  # ignore summer/winter time
        }

        r = requests.get(
            url,
            params=params,
            headers=self._auth_header
        ).json()

        return r['data']
