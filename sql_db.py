#general imports 
import sqlite3


def start_database():
    global base, cur

    base = sqlite3.connect('main.db')
    cur  = base.cursor()

    if base:
        print('Connected to the main.db')
    
    base.execute('CREATE TABLE IF NOT EXISTS balances(id TEXT, coin_code TEXT, amount TEXT)')

async def add_coin(state, id):
    async with state.proxy() as data:
        cur.execute(f"INSERT INTO balances VALUES ({id}, ?, ?)", tuple(data.values()))
        base.commit()

async def del_coin(id: str, coin_code: str):
    await cur.execute('DELETE FROM balances WHERE id == ? AND coin_code == ?', (id, coin_code))
    await base.commit()

async def get_balance(id):
    return cur.execute('SELECT * FROM balances WHERE id == ?', (id,))

