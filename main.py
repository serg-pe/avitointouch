# from net.pages_loader import PagesLoader
# from scraper.avito.avito_scraper import AvitoScraper

from aiogram.utils import executor

from tg_bot.bot import dp


if __name__ == '__main__':
    # url = 'https://www.avito.ru/kursk/rabota'
    # url = 'https://www.avito.ru/kursk/avtomobili'
    # url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426?radius=200'
    # url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426?f=ASgBAgECAkTgtg2MmSjitg3UqSgBRcaaDBZ7ImZyb20iOjAsInRvIjozMDAwMDB9&radius=200'
    # scraper = AvitoScraper()
    # # advertisements = scraper.scrap_advertisements(url)
    # start = time()
    # all_pages = scraper.load_all_pages(url)
    # print(len(all_pages))
    # end = time()
    # print(f'Serial execution time: {end - start}')
    
    # loader = PagesLoader()
    # loader.init_session(headers={
    #     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    #     'Accept-Language': 'ru'
    # })
    # loaded_page = loader.load_page(url)

    # scraper = AvitoScraper()
    # print('\n'.join([str(ad) for ad in scraper.scrap_ads(loaded_page)]))
    # print(scraper.scrap_pages_quantity(loaded_page))

    executor.start_polling(dp)