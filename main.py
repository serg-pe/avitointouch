from avito_scraper import AvitoScraper


if __name__ == '__main__':
    # url = 'https://www.avito.ru/kursk/rabota'
    url = 'https://www.avito.ru/kursk/avtomobili'
    # url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426?radius=200'
    # url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426?f=ASgBAgECAkTgtg2MmSjitg3UqSgBRcaaDBZ7ImZyb20iOjAsInRvIjozMDAwMDB9&radius=200'
    scraper = AvitoScraper()
    advertisements = scraper.scrap_advertisements(url)
    
    all_pages = scraper.laod_all_pages(url)
