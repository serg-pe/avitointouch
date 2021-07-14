from typing import List, Dict, Tuple
import re
from urllib import parse
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from datetime import datetime, timedelta

import requests
from sqlalchemy.sql.sqltypes import Date

from page import Page
from advertisement import Advertisement


class AvitoScraper(object):
    """Class for scraping."""
    
    def __init__(self, url: str) -> None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept-Language': 'ru'
        }

        self._session = requests.Session()
        self._session.headers.update(headers)
        self._session.get(url)

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

    def add_query_params(self, url: str, params: Dict[str, str]) -> str:
        """Updates URL's query parameters.
        Updates query parameters if similar in URL and params variable.

        Args:
            url (str): URL to add params
            params (Dict[str, str]): dictionary of params
        
        Reurns:
            str: URL with added parameters.
        """
        
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params.update(params)
        parsed_url = list(parsed_url)
        parsed_url[4] = urlencode(query_params)
        url = urlunparse(parsed_url)
        return url

    def _match_month_index(self, month: str) -> int:
        """Generates month index by its name, starting with 1.

        Args:
            month (str): month name

        Returns:
            int: month index.
        """
        months = (
            'январ', 
            'феврал', 
            'март', 
            'апрел', 
            'ма', 
            'июн',
            'июл',
            'август',
            'сентябр',
            'октябр',
            'декабр',
        )

        for month_index, month_name in enumerate(months, start=1):
            if re.search(month_name, month):
                return month_index

    def _parse_date_time(self, ad_date: str) -> datetime:
        """Parses date with template 'dd month_name hh:mm'.

        Args:
            ad_date (str): Avito's date representation

        Returns:
            datetime: Python's datetime representation.
        """
        date = datetime.now()
        day = re.findall(r'\d+', ad_date)[0]
        month_name = re.findall(r'[а-яА-Я]+', ad_date)[0]
        time = re.findall(r'(\d+:\d+)', ad_date)[0]
        hour, minute = time.split(':')
        month_index = self._match_month_index(month_name)
        date = date.replace(month=month_index, day=int(day), hour=int(hour), minute=int(minute))
        return date
    
    def _text_to_date(self, ad_date: str) -> datetime:
        """Parses Avito's section page advertisement posting time representation to datetime format.

        Args:
            ad_date (str): Avito's date representation

        Returns:
            datetime: Python's datetime representation.
        """
        date = datetime.now()
        if re.search(r'секунд', ad_date):
            return date

        time_scalar = int(re.findall(r'\d+', ad_date)[0])
        if re.search(r'минут', ad_date):
            date -= timedelta(minutes=time_scalar)
        elif re.search(r'час', ad_date):
            date -= timedelta(hours=time_scalar)
        elif re.search(r'(день)|(дней)|(дня)', ad_date):
            date -= timedelta(days=time_scalar)
        elif re.search(r'недел', ad_date):
            date -= timedelta(weeks=time_scalar)
        else:
            date = self._parse_date_time(ad_date)
        
        return date

    def scrap_page(self, url: str) -> Tuple[Advertisement]:
        """Scraps ADs from single web page.

        Args:
            url (str): web page URL

        Returns:
            Tuple[Advertisement]: ADs list.
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
            ad_date = ad.find('div', attrs={'data-marker': 'item-date'}).text
            ad_date = self._text_to_date(ad_date)
            advertisement = Advertisement(title=ad_title, price=ad_price, specific_params=ad_specific_params, url=ad_url, date=ad_date)
            advertisements.append(advertisement)

        return tuple(advertisements)

    def load_all_pages(self, url: str) -> List[Page]:
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

    def scrap_section(self, section_url: str, pages_quantity: int) -> Tuple[Advertisement]:
        """Scraps advertisements from given number of section's pages.

        Args:
            section_url (str): observerved section URL
            pages_quantity (int): quantity of parsed pages from section

        Returns:
            Tuple[Advertisement]: tuple of scraped advertisements.
        """

        first_page = self.load_page(section_url)
        all_pages_quantity = self.count_pages(first_page)
        if pages_quantity > all_pages_quantity:
            pages_quantity = all_pages_quantity

        advertisements = []
        for page_index in range(1, pages_quantity + 1):
            page_indexed_url = self.add_query_params(section_url, {'p': f'{page_index}'})
            advertisements += self.scrap_page(page_indexed_url)

        return tuple(advertisements)
