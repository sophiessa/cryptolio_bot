#general imports 
import sqlite3


def start_database():
    global base, cur

    base = sqlite3.connect('main.db')
    cur  = base.cursor()

    if base:
        print('connected to the main.db.......')
        
    #TODO: change to user_id, instead of using chat_id

    #a table for users
    base.execute('CREATE TABLE IF NOT EXISTS users(chat_id TEXT UNIQUE, username TEXT, language TEXT)')
    #a table for coin entries of users, consists of the chat_id (might change to user_id in the future), coin name and the amount of coins
    base.execute('CREATE TABLE IF NOT EXISTS wallet(chat_id TEXT, coin_code TEXT, amount INTEGER, )')


async def add_user(chat_id, username, language):
    await cur.execute(f'INSERT OR IGNORE INTO users VALUES ({chat_id}, {username}, {language})')
    base.commit()


async def get_lang(chat_id):
    await cur.execute(f'SELECT lang FROM users WHERE chat_id = {chat_id}')

async def add_coin(state, id, lang):
    async with state.proxy() as data:
        cur.execute(f"INSERT INTO balances VALUES ({id}, ?, ?, {lang})", tuple(data.values()))
        base.commit()

async def subract_coin(state, id):
    #TODO: subract certain amount from the balance of a certain coin
    pass

async def del_coin(id: str, coin_code: str):
    cur.execute(f"DELETE FROM balances WHERE id = {id} AND coin_code = '{coin_code}'")
    base.commit()

async def get_coins(id):
    return cur.execute(f'SELECT * FROM balances WHERE id == {id}')

