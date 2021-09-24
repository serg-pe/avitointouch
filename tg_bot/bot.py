from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from tg_bot.messages_templates import HELP_MESSAGE, SUPPORTED_COMMANDS


bot = Bot(token=getenv('TG_BOT_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=('start', 'help',))
async def send_help(msg: Message):
    return await msg.answer(f'{HELP_MESSAGE}\n{SUPPORTED_COMMANDS}', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton('Help', callback_data='/help'),
            InlineKeyboardButton('List', callback_data='/list'),
            InlineKeyboardButton('Unsubscribe', callback_data='/unsubscribe'),
        ))


@dp.message_handler(regexp='https://(www|m).avito.ru/[a-z]*/[a-z]*/(\S)*')
async def subscribe_avito(msg: Message):
    return await msg.answer(f'Avito link recieved')


@dp.message_handler()
async def send_command_not_found(msg: Message):
    return await msg.answer('Command not found')


# async def  
# @dp.callback_query_handler(text_contains='')
# async def menu(command: CallbackQuery):
#     return await 
