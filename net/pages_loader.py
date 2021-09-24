from typing import Dict
import requests


class PagesLoader:
    """Loader for websites"""

    def __init__(self, headers: Dict[str, str]=None) -> None:
        self._session = requests.Session()
        if headers:
            self._session.headers.update(headers)

    def load_page(self, url: str) -> str:
        response = self._session.get(url)
        return response.content
