from forex_python.converter import CurrencyRates
from telebot import *
from dotenv import *
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# connecting
import requests
try:
    response = requests.get('https://api.telegram.org', timeout=5)
    print("Соединение с Telegram API:", response.ok)
except Exception as e:
    print("Нет соединения:", e)

load_dotenv(r'secrets\.env')

cur = CurrencyRates()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'), skip_pending=True)

amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Введите сумму')
    bot.register_next_step_handler(message, error_check)

def error_check(message):
    mes = message.text.strip()
    try:
        mes = int(mes)
        if mes > 0:
            return summa(message)
        else:
            bot.send_message(message.chat.id, 'Ошибка! Введите сумму корректно')
            bot.register_next_step_handler(message, error_check)
    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибка! Введите сумму корректно')
        bot.register_next_step_handler(message, error_check)


def summa(message):
    global amount
    amount = message.text.strip()

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
    btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
    btn3 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
    btn4 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
    btn5 = types.InlineKeyboardButton('Другие валюты', callback_data='another')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)


@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    values = call.data.upper().split('/') # dont work with lower
    res = cur.convert(values[0], values[1], amount)
    bot.send_message(call.message.chat.id, f'{values[0]} В {values[1]}\n{amount} = {res}')
    bot.register_next_step_handler(call.message, error_check)

bot.infinity_polling()