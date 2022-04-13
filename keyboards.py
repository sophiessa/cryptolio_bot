from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
def basic_markup(lang='ru'):
    return {
        'ru': ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Мой баланс \U0001F4B0')).add(KeyboardButton('Моё портфолио \U0001F4CB')).add(KeyboardButton('Добавить крипту \U0001F4B5'), KeyboardButton('Удалить крипту \U0001F4C9')),
        'en': ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('My balance \U0001F4B0')).add(KeyboardButton('My portfolio \U0001F4CB')).add(KeyboardButton('Add crypto \U0001F4B5'), KeyboardButton('Delete crypto \U0001F4C9')),
        'kg': ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Баланс \U0001F4B0')).add(KeyboardButton('Портфолио \U0001F4CB')).add(KeyboardButton('Крипта кошуу \U0001F4B5'), KeyboardButton('Крипта очуруу \U0001F4C9'))
    }[lang]


def cancel_markup(lang='ru'):
    return {
        'ru': ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отменить \U00002716')),
        'en': ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Cancel \U00002716')),
        'kg': ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Жокко чыгаруу \U00002716')),
    }[lang]


def delete_coin_inline_markup(coin, lang='ru'):
    return {
        'ru': InlineKeyboardMarkup(resize=True).add(InlineKeyboardButton(text=f'Удалить {coin[1]}', callback_data=f'del{coin[1]}')),
        'en': InlineKeyboardMarkup(resize=True).add(InlineKeyboardButton(text=f'Delete {coin[1]}', callback_data=f'del{coin[1]}')),
        'kg': InlineKeyboardMarkup(resize=True).add(InlineKeyboardButton(text=f'{coin[1]} Очуруу', callback_data=f'del{coin[1]}')),
    }[lang]

cancelKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отменить'))