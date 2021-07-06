from typing import List, Dict
import re
from urllib import parse
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

import requests

from page import Page
from advertisement import Advertisement


class AvitoScraper(object):
    """Class for scraping."""
    
    def __init__(self) -> None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept-Language': 'ru'
        }

        self._session = requests.Session()
        self._session.headers = headers


    def load_page(self, url: str) -> Page:
        """Loads page by given url.

        Args:
            url (str): web page URL

        Returns:
            Page: web page structure.
        """

        request = self._session.get(url)
        page = Page(url, request.text)
        return page

    def count_pages(self, page: Page) -> int:
        """Counting ADs pages.

        Args:
            page (Page): loaded web page structure

        Returns:
            int: ADs pages quantity.
        """

        pagination = page.tree.find('div', attrs={'data-marker': 'pagination-button'})
        
        if not pagination:
            return 0

        pages_buttons = pagination.find_all('span')
        last_page_index_button = pages_buttons[-2]
        pages_quantity = re.findall(r'\d+', last_page_index_button['data-marker'])
        pages_quantity = int(pages_quantity[0])
        return pages_quantity

    def _add_query_params(self, url: str, params: Dict[str, str]) -> str:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params.update(params)
        parsed_url = list(parsed_url)
        parsed_url[4] = urlencode(query_params)
        url = urlunparse(parsed_url)
        return url

    def scrap_advertisements(self, url: str) -> List[Advertisement]:
        """Scraps ADs from single web page.

        Args:
            url (str): web page URL

        Returns:
            List[Advertisement]: ADs list.
        """

        advertisements = []
        page = self.load_page(url)
        advertisements_blocks = page.tree.find_all('div', attrs={'data-marker': 'item'})
        for ad in advertisements_blocks:
            link = ad.find('a', attrs={'data-marker': 'item-title'})
            ad_url = f"https://www.avito.ru{link['href']}"
            ad_title = link.find('h3').text
            ad_price = ad.find('meta', attrs={'itemprop': 'price'})['content']
            ad_specific_params = ad.find('div', attrs={'data-marker': 'item-specific-params'}).text
            advertisement = Advertisement(ad_url, ad_title, ad_price, ad_specific_params)
            advertisements.append(advertisement)

        return advertisements

    def laod_all_pages(self, url: str) -> List[Page]:
        """Loads all pages.

        Args:
            url (str): start url for section

        Returns:
            List[Page]: loaded pages to parse.
        """

        loaded_pages = []

        base_page = self.load_page(url)
        loaded_pages.append(base_page)

        pages_quantity = self.count_pages(base_page)
        for page_index in range(2, pages_quantity + 1):    
            url_with_page_index = self._add_query_params(url, {'p': f'{page_index}'})
            page = self.load_page(url_with_page_index)
            loaded_pages.append(page)
        
        return loaded_pages
