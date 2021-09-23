from typing import Dict
import requests


class PagesLoader:
    """Loader for websites"""

    def __init__(self) -> None:
        pass

    def init_session(self, headers: Dict[str, str]) -> str:
        self._session = requests.Session()
        self._session.headers.update(headers)

    def load_page(self, url: str) -> str:
        response = self._session.get(url)
        return response.content
