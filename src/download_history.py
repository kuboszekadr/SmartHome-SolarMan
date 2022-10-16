from .Endpoints.Account import Account
from .Endpoints.Station import Station


def download_history(app_id: str,
                     app_secret: str,
                     password: str,
                     email: str,
                     station_id: str,
                     date: str) -> None:

    account = Account(app_id, app_secret, password, email)
    account.get_token()

    station = Station(station_id, account)
    data = station.history(start_time=date)

    return data
