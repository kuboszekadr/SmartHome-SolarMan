import requests
import json

from typing import Dict


class Account:
    def __init__(self,
                 app_id: str,
                 app_secret: str,
                 password: str,
                 email: str) -> None:
        self._access_token: str = ''
        self._app_id: str = app_id
        self._app_secret: str = app_secret
        self._password: str = password
        self._email: str = email

    def get_token(self) -> str:
        url = "https://api.solarmanpv.com/account/v1.0/token"

        params = {
            'appId': self._app_id,
            'language': 'en'
        }
        payload = {
            "appSecret": self._app_secret,
            "email": self._email,
            "password": self._password
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Postman'
        }

        r = requests.post(
            url,
            params=params,
            headers=headers,
            json=payload
        )
        r = r.json()

        self._access_token = r['access_token']
        return self._access_token

    @property
    def auth_header(self) -> Dict:
        if self._access_token is None:
            raise ValueError("Not autheniticated yet")

        result = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self._access_token}",
            'User-Agent': 'Postman'
        }

        return result
