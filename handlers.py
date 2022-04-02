from os import stat
import requests, time
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from start_bot import dp, bot
import sql_db

headers = {
    'X-CMC_PRO_API_KEY': '1e7ca19f-f039-4cfc-b736-b29eea6adf3e',
}


class FSMClient(StatesGroup):
    id =        State()
    coin_code = State()
    amount =    State()

async def start(message: types.Message):
    await message.answer('Hi, what do you want to do?', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/add'), KeyboardButton('/balance'), KeyboardButton('/cancel'), KeyboardButton('/portfolio')))

async def show_balance(message: types.Message):
    coins = await sql_db.get_balance(message.from_user.id)
    sum = 0
    for coin in coins:
        parameters = {
            'amount': str(coin[2]),
            'symbol': str(coin[1]),
            'convert':'USD'
        }

        result = requests.get('https://pro-api.coinmarketcap.com/v1/tools/price-conversion', headers=headers, params=parameters)
        try:
            sum += float(result.json()['data']['quote']['USD']['price'])
        except KeyError:
            continue
    await message.answer(f'Сейчас: {time.localtime()[2]}/{time.localtime()[1]}/{time.localtime()[0]} | Время: {time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}')
    await message.answer("На вашем балансе %.2f$!" % sum)


async def add_coin(message: types.Message):
    await FSMClient.coin_code.set()
    await message.answer('Введите название криптовалюты!')

async def set_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['coin_code'] = message.text
    await FSMClient.next()
    await message.reply('Какое количество у вас имеется?')

async def set_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await sql_db.add_coin(state, message.from_user.id)
    await FSMClient.next()
    await message.reply('Добавлено в ваш кошелек!')
    await state.finish()


async def cancel(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state is None:
        return
    await state.finish()
    await message.reply('Загрузка успешно отменена!') 


async def portfolio(message: types.Message):
    coins = await sql_db.get_balance(message.from_user.id)
    for coin in coins:
        price = 0
        parameters = {
            'amount': str(coin[2]),
            'symbol': str(coin[1]),
            'convert':'USD'
        }

        result = requests.get('https://pro-api.coinmarketcap.com/v1/tools/price-conversion', headers=headers, params=parameters)
        try:
            price = float(result.json()['data']['quote']['USD']['price'])
        except KeyError:
            continue

        await message.answer(f'Crypto: {coin[1]} \nAmount: {coin[2]} \nPrice: %.2f$' % price)
    # await message.answer(f'Сейчас: {time.localtime()[2]}/{time.localtime()[1]}/{time.localtime()[0]} | Время: {time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}')
    # await message.answer("На вашем балансе %.2f$!" % sum)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel, commands=['cancel'], state='*')
    dp.register_message_handler(add_coin, commands=['add'], state=None)
    dp.register_message_handler(set_code, state=FSMClient.coin_code)
    dp.register_message_handler(set_amount, state=FSMClient.amount)

    dp.register_message_handler(show_balance, commands=['balance'])
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(portfolio, commands=['portfolio'])

