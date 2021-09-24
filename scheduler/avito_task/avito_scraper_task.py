import re

from scheduler.scraper_task import ScraperTask


class AvitoScraperTask(ScraperTask):
    """Task for avito scraper"""

    def generate_url_with_page(self, url: str, page_index: int) -> str:
        query_params = url.split('&')
        for query_param_index, query_param in enumerate(url.split('&')):
            if re.match('p=(\d)*', query_param):
                query_params[query_param_index] = f'p={page_index}'
                return '&'.join(query_params)

        return f'{url}&p={page_index}'