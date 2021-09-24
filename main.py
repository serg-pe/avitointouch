from asyncio import get_event_loop, sleep

from scraper.avito.avito_scraper import AvitoScraper
from scheduler.avito_task.avito_scraper_task import AvitoScraperTask

from aiogram.utils import executor

from tg_bot.bot import dp

from scheduler.scheduler import Scheduler


async def main():
    first_url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426?f=ASgBAgECAkTgtg2MmSjitg3UqSgBRcaaDBZ7ImZyb20iOjAsInRvIjozMDAwMDB9&radius=200'
    second_url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426-ASgBAgICAkTgtg2MmSjitg3UqSg?cd=1&f=ASgBAgECAkTgtg2MmSjitg3UqSgBRcaaDBZ7ImZyb20iOjAsInRvIjo1MDAwMDB9&radius=0&s=104'

    scheduler = Scheduler()
    get_event_loop().create_task(scheduler.add_task(first_url))
    await sleep(10)
    get_event_loop().create_task(scheduler.add_task(second_url))


if __name__ == '__main__':
    # url = 'https://www.avito.ru/kursk/rabota'
    # url = 'https://www.avito.ru/kursk/avtomobili'
    # url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426?radius=200'
    first_url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426?f=ASgBAgECAkTgtg2MmSjitg3UqSgBRcaaDBZ7ImZyb20iOjAsInRvIjozMDAwMDB9&radius=200'
    # scraper = AvitoScraper()
    # # advertisements = scraper.scrap_advertisements(url)
    # start = time()
    # all_pages = scraper.load_all_pages(url)
    # print(len(all_pages))
    # end = time()
    # print(f'Serial execution time: {end - start}')
    
    second_url = 'https://www.avito.ru/kursk/avtomobili/renault/logan_1426-ASgBAgICAkTgtg2MmSjitg3UqSg?cd=1&f=ASgBAgECAkTgtg2MmSjitg3UqSgBRcaaDBZ7ImZyb20iOjAsInRvIjo1MDAwMDB9&radius=0&s=104'

    # loader = PagesLoader(headers={
    #     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    #     'Accept-Language': 'ru'
    # })
    # loaded_page = loader.load_page(url)

    # scraper = AvitoScraper()
    # print('\n'.join([f'{ad}: {ad.price} - {ad.specific_params}' for ad in scraper.scrap_ads(loaded_page)]))
    # print(scraper.scrap_pages_quantity(loaded_page))

    # while True:

    
    get_event_loop().run_until_complete(main())
    executor.start_polling(dp)
    