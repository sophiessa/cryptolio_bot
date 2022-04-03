from aiogram.utils import executor

from start_bot import dp
import handlers
import sql_db

async def on_startup(_):
    sql_db.start_database()
    print('omratt_bot is started.....')

handlers.register_handlers(dp)

executor.start_polling(dp, on_startup=on_startup)
