
import sqlite3
import os
from telebot import *
from dotenv import *

# однопоточная обработка бота
import threading
db_lock = threading.Lock()



# Проверка на связь с TG API(не обязательно)
import requests
try:
    response = requests.get('https://api.telegram.org', timeout=5)
    print("Соединение с Telegram API:", response.ok)
except Exception as e:
    print("Нет соединения:", e)


# Создание базы данных если еще не создана
def init_db():
    with db_lock:
        con = sqlite3.connect("database.db", timeout=10, check_same_thread=False)
        try:
            cur = con.cursor()

            # Включаем WAL-режим ПЕРЕД созданием таблиц
            con.execute("PRAGMA journal_mode=WAL")

            cur.execute("""CREATE TABLE IF NOT EXISTS press(
                id INT
            )""")
            cur.execute("INSERT INTO press (id) VALUES (0)")
            con.commit() # Сохарнение изменений
        finally:
            con.close() # закончили работать с таблицей, очередь переходит другому пользователю

# Создаем базу данных
init_db()

# Подключение бота по API из secrets
load_dotenv(r'secrets\.env')
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))  #Токен бота

message_data_id = 0

# Запуск бота
@bot.message_handler(commands=['start'])
def start(message):
    global message_data_id
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Жми!', callback_data='general_button')
    markup.add(btn1)

    message_1 = bot.send_message(message.chat.id, 'Жми! Жми! Жми!', reply_markup=markup)
    message_data_id = message_1.message_id




@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global message_data_id
    if call.data == 'general_button':
        with db_lock:
            try:
                con = sqlite3.connect("database.db", check_same_thread=False)
                cur = con.cursor()
                cur.execute("UPDATE press SET id = id + 1")

                cur.execute("SELECT MAX(id) FROM press")
                res = cur.fetchone()

                bot.edit_message_text(f'Количество нажатий: {str(res)[1:-2]}', call.message.chat.id, message_data_id, reply_markup=call.message.reply_markup)
                con.commit()
            finally:
                con.close()





bot.infinity_polling()


