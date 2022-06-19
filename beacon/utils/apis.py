from typing import Dict, Mapping

import requests
from requests.adapters import HTTPAdapter, Retry

_URL_API = "https://api.coingecko.com/api/v3/"
_ENDPOINT_SIMPLE = "simple/"


class API:
    def __init__(self, url_base: str = _URL_API) -> None:

        self.url_base = url_base
        self.timeout = 10

        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.25, status_forcelist=[502, 503, 504])
        self.session.mount(self.url_base, HTTPAdapter(max_retries=retries))

    def __request(
        self, url: str, headers: Mapping[str, str], params: Mapping[str, str]
    ) -> Dict[str, Dict[str, str]]:

        response = self.session.get(
            url,
            headers=headers,
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_price(
        self,
        ids: str,
        vs_currencies: str = "usd",
        include_market_cap: bool = False,
        include_24hr_vol: bool = False,
        include_24hr_change: bool = False,
        include_last_updated_at: bool = False,
    ) -> Dict[str, Dict[str, str]]:

        url = f"{_URL_API}{_ENDPOINT_SIMPLE}price"
        headers = {"accept": "application/json"}
        params = {
            "ids": ids,
            "vs_currencies": vs_currencies,
            "include_market_cap": str(include_market_cap).lower(),
            "include_24hr_vol": str(include_24hr_vol).lower(),
            "include_24hr_change": str(include_24hr_change).lower(),
            "include_last_updated_at": str(include_last_updated_at).lower(),
        }

        return self.__request(url, headers, params)

    def get_coin(
        self,
        id: str,
        localization: bool = False,
        tickers: bool = False,
        market_data: bool = False,
        community_data: bool = False,
        developer_data: bool = False,
        sparkline: bool = False,
    ) -> Dict[str, Dict[str, str]]:

        url = f"{_URL_API}coins/{id}"
        headers = {"accept": "application/json"}
        params = {
            "localization": str(localization).lower(),
            "tickers": str(tickers).lower(),
            "market_data": str(market_data).lower(),
            "community_data": str(community_data).lower(),
            "developer_data": str(developer_data).lower(),
            "sparkline": str(sparkline).lower(),
        }

        return self.__request(url, headers, params)
