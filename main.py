from avito_scraper import AvitoScraper


if __name__ == '__main__':
    # url = 'https://www.avito.ru/kursk/rabota'
    url = 'https://www.avito.ru/kursk/avtomobili'
    # url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426?f=ASgBAgECAkTgtg2MmSjitg3UqSgBRcaaDBV7ImZyb20iOjAsInRvIjoxMjAwMH0&radius=200'
    scraper = AvitoScraper()
    scraper.scrap_advertisements(url)
