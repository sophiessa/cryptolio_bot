#general imports 
import sqlite3


def start_database():
    global base, cur

    base = sqlite3.connect('main.db')
    cur  = base.cursor()

    if base:
        print('connected to the main.db.......')
    
    base.execute('CREATE TABLE IF NOT EXISTS balances(id TEXT, coin_code TEXT, amount TEXT)')

async def add_coin(state, id):
    async with state.proxy() as data:
        cur.execute(f"INSERT INTO balances VALUES ({id}, ?, ?)", tuple(data.values()))
        base.commit()

async def subract_coin(state, id):
    #TODO: subract certain amount from the balance of a certain coin
    pass

async def del_coin(id: str, coin_code: str):
    cur.execute(f"DELETE FROM balances WHERE id = {id} AND coin_code = '{coin_code}'")
    base.commit()

async def get_coins(id):
    return cur.execute(f'SELECT * FROM balances WHERE id == {id}')

