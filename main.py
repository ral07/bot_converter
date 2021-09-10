import telebot

import extensions
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
active_step = 0
BASE = ""
QUOTE = ""
AMOUNT = 0


@bot.message_handler(commands=['start'])
def start_commands(message):
    bot.send_message(message.from_user.id, extensions.MESSAGES.HELP.value)
    first_valute(message)


@bot.message_handler(commands=['help'])
def start_commands(message):
    bot.send_message(message.from_user.id, extensions.MESSAGES.HELP.value)


@bot.message_handler(commands=['values'])
def start_commands(message):
    bot.send_message(message.from_user.id, extensions.MESSAGES.VALUES.value)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if active_step == 3:
        global AMOUNT
        AMOUNT = message.text
    try:
        if not AMOUNT.isdigit():
            raise extensions.APIException(extensions.ERRORS.INCORRECT_AMOUNT)
    except extensions.APIException as mr:
        bot.send_message(message.from_user.id, mr.error.value)
        if mr.error == extensions.ERRORS.INCORRECT_AMOUNT:
            amount_valute(message)
        return
    convert = extensions.Convertor(BASE, QUOTE, int(AMOUNT))
    bot.send_message(message.from_user.id, AMOUNT + " " + BASE + " = " + str(
        convert.get_price()) + " " + QUOTE)


def keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_rub = types.InlineKeyboardButton(text='RUB', callback_data='RUB')
    keyboard.add(key_rub)
    key_usd = types.InlineKeyboardButton(text='USD', callback_data='USD')
    keyboard.add(key_usd)
    key_eur = types.InlineKeyboardButton(text='EUR', callback_data='EUR')
    keyboard.add(key_eur)
    return keyboard


def first_valute(message):
    global active_step
    active_step = 1
    bot.send_message(message.from_user.id, text=extensions.MESSAGES.FIRST_VALUTE.value, reply_markup=keyboard())


def second_valute(message):
    global active_step
    active_step = 2
    bot.send_message(message.chat.id, text=extensions.MESSAGES.SECOND_VALUTE.value, reply_markup=keyboard())


def amount_valute(message):
    global active_step
    active_step = 3
    bot.send_message(message.chat.id, text=extensions.MESSAGES.AMOUNT_VALUTE.value)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if active_step == 1:
        global BASE
        BASE = call.data
        second_valute(call.message)
    elif active_step == 2:
        global QUOTE
        QUOTE = call.data
        amount_valute(call.message)


bot.polling(none_stop=True, interval=0)
