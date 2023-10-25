import aiosqlite

async def start_database():
    async with aiosqlite.connect('main.db') as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                chat_id TEXT UNIQUE,
                username TEXT,
                language TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS wallets(
                user_id INTEGER,
                coin_code TEXT,
                amount INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        print('Connected to the main.db and ensured tables exist...')


#Functions for user table

async def add_user(user_id, chat_id, username, language):
    async with aiosqlite.connect('main.db') as db:
        await db.execute('INSERT INTO users (user_id, chat_id, username, language) VALUES (?, ?, ?, ?)', (user_id, chat_id, username, language))
        await db.commit()


async def get_lang(user_id):
    async with aiosqlite.connect('main.db') as db:
        print(f'THE TYPE OF USER ID IS {type(user_id)}')
        cursor = await db.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
        
        row = await cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
        



#Functions for wallet table

async def add_coin(state, user_id):
    async with aiosqlite.connect('main.db') as db:
        async with state.proxy() as data:
            await db.execute('INSERT INTO wallets (user_id, coin_code, amount) VALUES (?, ?, ?)', (user_id, data['coin_code'], data['amount']))
            await db.commit()


async def get_coins(user_id, coin_code):
    async with aiosqlite.connect('main.db') as db:
        cursor = await db.execute('SELECT * FROM wallets WHERE user_id = ? AND coin_code = ?', (user_id, coin_code))
        row = await cursor.fetchone()
        if row:
            return row[0]
        else:
            return None
        
async def del_coin(user_id, coin_code):
    async with aiosqlite.connect('main.db') as db:
        await db.execute('DELETE FROM wallets WHERE user_id = ? AND coin_code = ?', (user_id, coin_code))
        await db.commit()
        