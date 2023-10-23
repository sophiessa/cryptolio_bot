def start_message(lang='ru'):
    return {
        'ru': 'Здравствуйте, что бы вы хотели сделать?',
        'en': 'Hi, what do you want to do?',
        'kg': 'KGZ START MESSAGE',
    }[lang]

def add_coin_code(lang='ru'):
    return {
        'ru': 'Введите код криптовалюты (BTC, XRP, SOL и т.д.)',
        'en': 'Type in the code of the cryptocurrency (BTC, XRP, SOL ...)',
        'kg': 'Криптоакчанын кодун жазыныз (BTC, XRP, SOL и ж.б.)',
    }[lang]

def add_coin_amount(lang='ru'):
    return {
        'ru': 'Введите количество криптовалюты',
        'en': 'How much do you have?',
        'kg': 'Криптоакчанын саны канча',
    }[lang]

def add_coin_added(lang='ru'):
    return {
        'ru': 'Добавлено!',
        'en': 'Added!',
        'kg': 'Кошулду!',
    }[lang]

def add_coin_cancel(lang='ru'):
    return {
        'ru': 'Отменено!',
        'en': 'Canceled!',
        'kg': 'Жокко чыкты!',
    }[lang]

def show_portfolio_text(coin, price, lang='ru'):
    return {
        'ru': f'Криптовалюта: {coin[1]} \nКоличество: {coin[2]} \nВ Доллараx: %.2f$' % price,
        'en': f'Cryptocurrency: {coin[1]} \nAmount: {coin[2]} \nIn $USD: %.2f$' % price,
        'kg': f'Криптоакча: {coin[1]} \nСаны: {coin[2]} \nДолларга которгондо: %.2f$' % price,
    }[lang]

def show_balance_text(sum, lang='ru'):
    return {
        'ru': "На вашем балансе есть %.2f$!" % sum,
        'en': "You have %.2f$ in your balance!" % sum,
        'kg': "Сиздин балансынызда %.2f$ бар!" % sum,
    }[lang]

def delete_coin_text(lang='ru'):
    return {
        'ru': 'Выберите криптовалюту которую вы хотите удалить!',
        'en': 'Choose crypto that you want to delete!',
        'kg': 'Очургунуз келгенди танданыз!',
    }[lang]

def delete_coin_inline_text(coin, lang='ru'):
    return {
        'ru': f'Криптовалюта: {coin[1]} \nКоличество: {coin[2]}',
        'en': f'Cryptocurrency: {coin[1]} \nAmount: {coin[2]}',
        'kg': f'Криптоакча: {coin[1]} \nСаны: {coin[2]}',
    }[lang]


def choose_language(lang='ru'):
    return {
        'ru': f'VYBERITE YAZYK',
        'en': f'CHOOSE A LANGUAGE',
        'kg': f'TIL TANDANYZ',
    }[lang]