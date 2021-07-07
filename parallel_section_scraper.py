from typing import Tuple

from math import ceil
from os import cpu_count
from multiprocessing import Pool
from threading import Thread

from page import Page
from avito_scraper import AvitoScraper


class ParallelSectionScraper(object):
    """Section scraper. Loads and parses all pages for selected category.

    Section is the first page for selected category.
    """

    def __init__(self, section_url: str, processes: int=None):
        self._processes_count = processes if processes else cpu_count()
        self._section_url = section_url
        
    def _split_pages(self, pages_quantity: int) -> Tuple[range]:
        """Divides pages indexes into equal parts beetwen processes.
        For example, 100 pages divides at parts (13, 13, 13, 13, 12, 12, 12, 12) beetwen 8 processes.

        Args:
            pages_quantity (int): number of pages in section

        Returns:
            Tuple[range]: tuple of ranges with start and end pages indexes.
        """
        chunks = []

        current_start_index = 0
        for process_index in range(self._processes_count):
            current_chunk_size = ceil((pages_quantity - current_start_index) / (self._processes_count - process_index))
            current_end_index = current_start_index + current_chunk_size
            chunks.append(range(current_start_index, current_end_index))
            current_start_index = current_end_index

        return tuple(chunks)

    def _scrap_advertisements(self, chunk: Tuple[range]):
        """Scraps ADs for all pages in given chunk.

        This method works inside processes.

        Args:
            chunk (Tuple[range]): pages range to parse
        """
        scraper = AvitoScraper()
        advertisements = []
        for i in chunk:
            url_with_page_index = scraper.add_query_params(self._section_url, {'p': f'{i}'})
            advertisements += scraper.scrap_advertisements(url_with_page_index)
        print(len(advertisements))

    def scrap(self):
        """Scraps ADs in parallel.
        """
        scraper = AvitoScraper()
        section_page = scraper.load_page(self._section_url)
        pages_quantity = scraper.count_pages(section_page)

        pages_ranges = self._split_pages(pages_quantity)
        pool = Pool(self._processes_count)
        pool.map(self._scrap_advertisements, pages_ranges)
