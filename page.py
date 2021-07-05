import requests
import bs4


class Page(object):
    """Web page HTML and tree data."""
    def __init__(self, url: str, site_html: str) -> None:
        self._url = url
        self._html = site_html
        self._tree = bs4.BeautifulSoup(self.html, 'html.parser')

    @property
    def url(self) -> str:
        return self._url

    @property
    def html(self) -> str:
        return self._html

    @property
    def tree(self) -> bs4.BeautifulSoup:
        return self._tree
