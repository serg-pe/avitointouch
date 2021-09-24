from sqlalchemy.sql.expression import or_
from models.models import Advertisement
from typing import Collection
from abc import ABC, abstractmethod
from asyncio import sleep
from datetime import timedelta

from sqlalchemy import literal

from scraper.scraper import Scraper
from net.pages_loader import PagesLoader
from db.db_connection import get_session


class ScraperTask:

    def __init__(self, scraper: Scraper, url: str):
        self._scraper = scraper
        self._url = url

    @abstractmethod
    def generate_url_with_page(self, url: str, page_index: int) -> str:
        """Generates URL with page index.

        Args:
            url (str): base URL
            page_index (int): index of loaded page

        Returns:
            str: URL with page index.
        """
        pass

    async def schedule(self) -> None:
        """Schedules in infinite loop loading pages and scraper with sleep interval.
        """
        loader = PagesLoader({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept-Language': 'ru',
        })
        started = True

        while True:
            print(f'{self._url} started')
            page_content = loader.load_page(self._url)
            pages_quantity = self._scraper.scrap_pages_quantity(page_content)
            if started:
                pages_quantity = 3 if pages_quantity >= 3 else pages_quantity
                started = False

            page_index = 1
            while page_index <= pages_quantity:
                advertisements = self._scraper.scrap_ads(page_content)

                if not self._write_ads_to_db(advertisements):
                    break
                
                page_index += 1
                page_content = loader.load_page(self.generate_url_with_page(self._url, page_index))

            await sleep(60)   

    def _write_ads_to_db(self, loaded_advertisements: Collection[Advertisement]) -> bool:
        """Writes loaded advertisements to database and proves these advertisements are new.

        Args:
            loaded_advertisements (Collection[Advertisement]): loaded advertisements

        Returns:
            bool: Returns True if page contains new advertisements, else False.
        """
        was_written = False

        with get_session() as db:
            for ad in loaded_advertisements:
                if not db.query(literal(True)).filter(db.query(Advertisement).filter(
                        or_(Advertisement.date > ad.date - timedelta(seconds=10), Advertisement.date < ad.date + timedelta(seconds=10)),
                        Advertisement.title == ad.title
                ).exists()).scalar():
                    was_written = True
                    db.add(ad)

            if was_written:
                db.commit()
  
        return was_written
