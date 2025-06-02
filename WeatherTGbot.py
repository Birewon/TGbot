import requests
from telebot import *
from dotenv import *
import os

load_dotenv(r'secrets\.env')
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
if not bot:
    raise ValueError("Токен не найден в .env!")
API = os.getenv('API_WEATHER')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Укажи название города')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    import json
    inf = json.loads(res.text)
 
    bot.reply_to(message, f'Погода сейчас: {inf["main"]["temp"]}')

bot.infinity_polling()