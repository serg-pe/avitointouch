from typing import Tuple
import re
from datetime import datetime, timedelta

import bs4

from scraper.scraper import Scraper
from models.advertisement import Advertisement


class AvitoScraper(Scraper):

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

    def scrap_pages_quantity(self, page_content) -> int:
        page_content = bs4.BeautifulSoup(page_content, 'html.parser')
        pagination = page_content.find('div', attrs={'data-marker': 'pagination-button'})
        
        if not pagination:
            return 0

        pages_quantity = int(pagination.find_all('span')[-2].next) # element inside span is text
        return pages_quantity

    def scrap_ads(self, page_content: str) -> Tuple[Advertisement]:
        page_content = bs4.BeautifulSoup(page_content, 'html.parser')
        advertisements = []
        for ad_block in page_content.find_all('div', attrs={'data-marker': 'item'}):
            ad_url = f'https://www.avito.ru{ad_block.find("a", attrs={"data-marker": "item-title"})["href"]}'
            ad_title = ad_block.find('h3').text
            ad_price = ad_block.find('meta', attrs={'itemprop': 'price'})['content']
            specific_params_element = ad_block.find('div', attrs={'data-marker': 'item-specific-params'})
            ad_specific_params = specific_params_element.text if specific_params_element else None
            ad_date = self._text_to_date(ad_block.find('div', attrs={'data-marker': 'item-date'}).text)
            
            advertisements.append(Advertisement(
                title=ad_title,
                price=ad_price,
                specific_params=ad_specific_params, 
                url=ad_url, date=ad_date
            ))

        return tuple(advertisements)
