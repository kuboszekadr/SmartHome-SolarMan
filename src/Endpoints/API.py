class API():
    URL = "https://api.solarmanpv.com/{api}"

    def __init__(self, name: str) -> None:
        self._url = self.URL.format(api=name.lower())

    def url(self) -> str:
        return self._url

    def endpoint_url(self, endpoint: str) -> str:
        result = f"{self._url}/v1.0/{endpoint}?language=en"
        return result
