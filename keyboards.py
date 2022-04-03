from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

addOrDeleteKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Добавить Монету'), KeyboardButton('Удалить Монету')).add(KeyboardButton('Отменить'))

seeBalancePortfoliKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Мой баланс')).add(KeyboardButton('Моё портфолио')).add(KeyboardButton('Добавить Монету'), KeyboardButton('Удалить Монету'), KeyboardButton('Отменить'))

cancelKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отменить'))