# Чек-лист оценки проекта:
import telebot
from gpt import create_promt, ask_gpt, count_tokens_in_dialogue
from peremen import *


bot = telebot.TeleBot(API)

current_options = {}
exist_options = {
    'genres': ["Детектив", 'Мистика', "Фентези"],
    'characters': ["Ибрагим (Дальнобойщик)", 'Патрик', "Рик", "Бетмен"],
    'settings': ["Cyberpunk 2077", 'Тёмное фентази', "Постапокалипсис", "Преступный город"]
}



def create_keyboard(options):
    buttons = []
    for opt in options:
        buttons.append(telebot.types.KeyboardButton(text=opt))

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def can_text(user_id):
    bot.send_message(user_id, text='Привет! К сожалению, существует ограничение на количество пользователей '
                                   'и сессий для каждого из пользователей, :( Ты не сможешь составить сценарий')



@bot.message_handler(commands=['start'])
def start(message):
    global current_options
    user_id = message.from_user.id

    if len(current_options) >= MAX_USERS:
        can_text(user_id)
        return

    bot.send_message(user_id, text='Привет, я - бот-сценарист. Ты можешь выбрать жанр, '
                                   'героя и сеттинг, а я напишу сценарий для тебя. Нажми на кнопку /write_scen',
                     reply_markup=create_keyboard(['/write_scen']))

    if user_id not in current_options:
        current_options[user_id] = {
            'session': 1,
            'genre': '',
            'character': '',
            'setting': '',
            'additionally': '',
            'tokens': 0,
            'debug': False
        }




@bot.message_handler(commands=['write_scen'])
def write_scen(message):
    global exist_options

    user_id = message.from_user.id

    if len(current_options) >= MAX_USERS:
        can_text(user_id)
        return

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("debug", callback_data="debug"))

    bot.send_message(user_id, text='Для начала выбери жанр',
                     reply_markup=create_keyboard(exist_options['genres']))
    bot.send_message(user_id, text='Если хочешь, чтобы тебе приходили сообщения с информацией о том'
                                   'что происходит в боте, то нажми на debug (но лучше не надо)',
                     reply_markup=keyboard)

    bot.register_next_step_handler(message, genre)

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global current_options
    if call.data == 'debug':
        current_options[call.from_user.id]['debug'] = True
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Включен режим дебага')

def genre(message):
    global current_options
    global exist_options

    genre = message.text
    user_id = message.from_user.id

    if genre not in exist_options['genres']:
        bot.send_message(user_id, text='Выбран несуществующий жанр')
        write_scen(message)
        return

    if current_options[user_id]['debug']:
        bot.send_message(user_id, text=f'Выбран жанр "{genre}"')

    current_options[user_id]['genre'] = genre
    bot.send_message(user_id, text='Теперь выбери героя, с которым должны происходить всякие действия',
                     reply_markup=create_keyboard(exist_options['characters']))
    bot.register_next_step_handler(message, character)


def character(message):
    global current_options
    global exist_options

    character = message.text
    user_id = message.from_user.id

    if character not in exist_options['characters']:
        bot.send_message(user_id, text='Выбран несуществующий персонаж')
        write_scen(message)
        return

    if current_options[user_id]['debug']:
        bot.send_message(user_id, text=f'Выбран герой "{character}"')

    current_options[user_id]['character'] = character
    bot.send_message(user_id, text='Теперь выбери сеттинг',
                     reply_markup=create_keyboard(exist_options['settings']))
    bot.register_next_step_handler(message, setting)


def setting(message):
    global current_options
    global exist_options

    setting = message.text
    user_id = message.from_user.id

    if setting not in exist_options['settings']:
        bot.send_message(user_id, text='Выбран несуществующий сеттинг')
        write_scen(message)
        return

    if current_options[user_id]['debug']:
        bot.send_message(user_id, text=f'Выбран сеттинг "{setting}"')

    current_options[user_id]['setting'] = setting
    bot.send_message(user_id, text='Все выбрано. Нужно ли внести дополнительную информацию? Тогда напиши ее!'
                                   'Если же дополнять не хочешь, то просто вызови команду /begin',
                     reply_markup=create_keyboard(['/begin']))
    bot.register_next_step_handler(message, begin)

@bot.message_handler(commands=['begin'])
def begin(message):
    global current_options

    user_id = message.from_user.id
    text = message.text

    if len(current_options) >= MAX_USERS:
        can_text(user_id)
        return

    if user_id not in current_options:
        bot.send_message(user_id, text='Ты пока не регистрировался и не выбирал, '
                                       'из каких частей будет состоять твой сценарий. Тыкни на /start',
                         reply_markup=create_keyboard(['/start']))
        return

    if current_options[user_id]['session'] > MAX_SESSIONS:
        can_text(user_id)
        return

    if text != '/begin':
        current_options[user_id]['additionally'] = text
        bot.send_message(user_id, text='Ну теперь точно жми /begin', reply_markup=create_keyboard(['/begin']))
        return

    promt = create_promt(current_options, user_id)

    bot.send_message(user_id, text='Генерирую...')

    if current_options[user_id]['debug']:
        bot.send_message(user_id, text=f'Происходит генерация ответа')

    collection = [
        {'role': 'system', 'text': promt}
    ]

    result, status = ask_gpt(collection)

    if not status:
        bot.send_message(user_id, text='Произошла ошибка, попробуйте снова чуть позже',
                         reply_markup=create_keyboard(['/start']))
        if current_options[user_id]['debug']:
            bot.send_message(user_id, text=f'Произошла ошибка {result}')
        return

    collection.append({'role': 'assistant', 'text': result})
    tokens = count_tokens_in_dialogue(collection)
    current_options[user_id]['tokens'] += tokens

    if current_options[user_id]['tokens'] >= MAX_TOKENS_IN_SESSION:
        bot.send_message(user_id, text=result)
        bot.send_message(user_id, text='Количество токенов в рамках текущей сессии закончилось. '
                                       'Началась следующая сессия. Хотел бы попробовать снова?',
                         reply_markup=create_keyboard(['/write_scen']))
        current_options[user_id]['session'] += 1
        return

    bot.send_message(user_id, text=result)
    bot.send_message(user_id, text='Хотел бы попробовать снова? Нажми /write_scen',
                     reply_markup=create_keyboard(['/write_scen']))


if __name__ == '__main__':
    bot.infinity_polling()





