from currency_converter import currency_converter, CurrencyConverter
from telebot import *
from dotenv import *
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import requests
try:
    response = requests.get('https://api.telegram.org', timeout=5)
    print("Соединение с Telegram API:", response.ok)
except Exception as e:
    print("Нет соединения:", e)

load_dotenv(r'secrets\.env')
cur = CurrencyConverter()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

amount = 0

bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Введите сумму")
    bot.reply_to(message, summa)

def summa(message):
    global amount
    amount = message.text.strip()
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        btn1 = InlineKeyboardButton('USD/EUR', callback_data='usd/eur'),
        btn2 = InlineKeyboardButton('EUR/USD', callback_data='eur/usd'),
        btn3 = InlineKeyboardButton('RUB/USD', callback_data='rub/usd'),
        btn4 =InlineKeyboardButton('USD/RUB', callback_data='usd/rub'),
        btn5 = InlineKeyboardButton('Другие валюты', callback_data='another')
    )
    bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)

bot.infinity_polling()