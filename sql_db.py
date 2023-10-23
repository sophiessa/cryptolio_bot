import aiosqlite

async def start_database():
    async with aiosqlite.connect('main.db') as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT UNIQUE,
                username TEXT,
                language TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS wallet(
                user_id INTEGER,
                chat_id TEXT,
                coin_code TEXT,
                amount INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        print('Connected to the main.db and ensured tables exist...')

async def add_user(chat_id, username, language):
    async with aiosqlite.connect('main.db') as db:
        await db.execute('INSERT INTO users (chat_id, username, language) VALUES (?, ?, ?)', (chat_id, username, language))
        await db.commit()


async def get_lang(chat_id):
    async with aiosqlite.connect('main.db') as db:
        cursor = await db.execute('SELECT language FROM users WHERE chat_id = ?', (chat_id))
        row = await cursor.fetchone()
        if row:
            return row[0]
        else:
            return None