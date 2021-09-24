from typing import List
import re

from scheduler.scraper_task import ScraperTask
from scheduler.avito_task.avito_scraper_task import AvitoScraperTask
from scraper.avito.avito_scraper import AvitoScraper


class Scheduler:
    '''Sceduler for Scraper Tasks'''

    def __init__(self) -> None:
        pass

    async def add_task(self, url: str) -> None:
        if re.match('(https://)?(www|m).avito.ru(\D)*', url):
            scraper_task = AvitoScraperTask(AvitoScraper(), url)
        else:
            raise ValueError(f'No task for {url}')

        await scraper_task.schedule()

    async def start(self):
        for task in self._tasks:
            await task.schedule()
