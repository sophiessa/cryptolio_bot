from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

addOrDeleteKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Добавить'), KeyboardButton('Удалить')).add(KeyboardButton('Отменить'))