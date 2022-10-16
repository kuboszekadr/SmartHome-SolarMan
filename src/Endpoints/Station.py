from datetime import date
import requests

from .Account import Account
from .API import API


class Station(API):
    def __init__(self, id: int, account: Account) -> None:
        self._id = id
        self._account = account
        super().__init__(Station.__name__)

    def history(self,
                time_type: int = 1,
                start_time: date = date.today(),
                end_time: date = None) -> dict:
        payload = {
            "stationId": self._id,
            "timeType": time_type,
            "startTime": start_time.strftime('%Y-%m-%d')
        }

        if end_time is not None:
            payload["endTime"] = end_time

        header = self._account.auth_header
        url = self.endpoint_url('history')

        r = requests.post(
            url=url,
            headers=header,
            json=payload
        )

        result = r.json()
        return result
