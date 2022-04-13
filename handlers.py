#general imports
import requests, time, os, dotenv

#aiogram imports
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

#local imports
from start_bot import dp, bot
import sql_db
import keyboards as kbs
import texts as txs

dotenv.load_dotenv()

headers = {
    'X-CMC_PRO_API_KEY': os.getenv('COINMARKETCAP_TOKEN'),
}


class FSMClient(StatesGroup):
    id =        State()
    coin_code = State()
    amount =    State()

async def start(message: types.Message):
    lang = message.from_user.language_code
    text = txs.start_message(lang)
    start_keyboard = kbs.basic_markup(lang)
    await message.answer(text, reply_markup=start_keyboard)

async def add_coin(message: types.Message):
    lang = message.from_user.language_code
    text = txs.add_coin_code(lang)
    cancel_keyboard = kbs.cancel_markup(lang)
    await FSMClient.coin_code.set()
    await message.answer(text=text, reply_markup=cancel_keyboard)

async def set_code(message: types.Message, state: FSMContext):
    #TODO: implement merge of the same cryptocurrency
    lang = message.from_user.language_code
    text = txs.add_coin_amount(lang)
    cancel_keyboard = kbs.cancel_markup(lang)
    async with state.proxy() as data:
        data['coin_code'] = message.text
    await FSMClient.next()
    await message.reply(text=text, reply_markup=cancel_keyboard)

async def set_amount(message: types.Message, state: FSMContext):
    lang = message.from_user.language_code
    text = txs.add_coin_added(lang)
    basic_keyboard = kbs.basic_markup(lang)
    async with state.proxy() as data:
        data['amount'] = message.text
    await sql_db.add_coin(state, message.from_user.id)
    await FSMClient.next()
    await message.reply(text=text, reply_markup=basic_keyboard)
    await state.finish()


async def cancel(message: types.Message, state: FSMContext):
    lang = message.from_user.language_code
    text = txs.add_coin_cancel(lang)
    basic_keyboard = kbs.basic_markup(lang)
    curr_state = await state.get_state()
    if curr_state is None:
        return
    await state.finish()
    await message.reply(text=text, reply_markup=basic_keyboard) 


async def show_portfolio(message: types.Message):
    lang = message.from_user.language_code
    coins = await sql_db.get_coins(message.from_user.id)
    for coin in coins:
        price = 0
        parameters = {
            'amount' : str(coin[2]),
            'symbol' : str(coin[1]),
            'convert': 'USD'
        }

        result = requests.get('https://pro-api.coinmarketcap.com/v1/tools/price-conversion', headers=headers, params=parameters)
        try:
            price = float(result.json()['data']['quote']['USD']['price'])
        except KeyError:
            continue
        
        text = txs.show_portfolio_text(coin, price, lang)
        basic_keyboard = kbs.basic_markup(lang)
        await message.answer(text=text, reply_markup=basic_keyboard)
    

async def show_balance(message: types.Message):
    lang = message.from_user.language_code
    coins = await sql_db.get_coins(message.from_user.id)
    sum = 0
    for coin in coins:
        parameters = {
            'amount' : str(coin[2]),
            'symbol' : str(coin[1]),
            'convert': 'USD'
        }

        result = requests.get('https://pro-api.coinmarketcap.com/v1/tools/price-conversion', headers=headers, params=parameters)
        try:
            sum += float(result.json()['data']['quote']['USD']['price'])
        except KeyError:
            continue
    # await message.answer(f'Сейчас: {time.localtime()[2]}/{time.localtime()[1]}/{time.localtime()[0]} | Время: {time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}')
    text = txs.show_balance_text(sum, lang)
    basic_keyboard = kbs.basic_markup(lang)
    await message.answer(text=text, reply_markup=basic_keyboard)

async def delete_coin(message: types.Message):
    lang = message.from_user.language_code
    text = txs.delete_coin_text(lang)
    coins = await sql_db.get_coins(message.from_user.id)
    await message.reply(text=text)
    for coin in coins:
        inline_text = txs.delete_coin_inline_text(coin, lang)
        delete_inline_keyboard = kbs.delete_coin_inline_markup(coin, lang)
        await message.answer(text=inline_text, reply_markup=delete_inline_keyboard)

async def deletion_callback(callback_query: types.CallbackQuery):
    await sql_db.del_coin(callback_query.from_user.id, callback_query.data.replace('del', ''))
    await callback_query.answer(text='Delted!')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    
    dp.register_message_handler(cancel, Text(contains='\U00002716'), state='*')
    dp.register_message_handler(add_coin, Text(contains='\U0001F4B5'), state=None)
    dp.register_message_handler(set_code, state=FSMClient.coin_code)
    dp.register_message_handler(set_amount, state=FSMClient.amount)

    dp.register_message_handler(delete_coin, Text(contains='\U0001F4C9'))
    dp.register_callback_query_handler(deletion_callback, Text(startswith='del'))

    dp.register_message_handler(show_balance, Text(contains='\U0001F4B0'))
    dp.register_message_handler(show_portfolio, Text(contains='\U0001F4CB'))

