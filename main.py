from avito_scraper import AvitoScraper
from time import time
from parallel_section_scraper import ParallelSectionScraper


if __name__ == '__main__':
    # url = 'https://www.avito.ru/kursk/rabota'
    url = 'https://www.avito.ru/kursk/avtomobili'
    # url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426?radius=200'
    # url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426?f=ASgBAgECAkTgtg2MmSjitg3UqSgBRcaaDBZ7ImZyb20iOjAsInRvIjozMDAwMDB9&radius=200'
    # scraper = AvitoScraper()
    # # advertisements = scraper.scrap_advertisements(url)
    # start = time()
    # all_pages = scraper.load_all_pages(url)
    # print(len(all_pages))
    # end = time()
    # print(f'Serial execution time: {end - start}')
    
    loader = ParallelSectionScraper(url)
    
    start = time()
    loader.scrap()
    end = time()
    print(f'Parallel execution time: {end - start}')
