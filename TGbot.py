from telebot import types
import telebot
import time
import os
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardRemove

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))  #Токен бота




@bot.message_handler(commands=['start'])
def start_1(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    btn1 = types.KeyboardButton('🍎 Яблоко')
    btn2 = types.KeyboardButton('🍌 Банан')
    btn3 = types.KeyboardButton('🍊 Апельсин')
    btn4 = types.KeyboardButton('🥒 К овощам')
    btn5 = types.KeyboardButton('❌ Скрыть')
    markup.add(btn1, btn2, btn3, btn4, btn5)

    bot.send_message(message.chat.id, "Какой фрукт вам нравится больше всего?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['🍎 Яблоко', '🍌 Банан', '🍊 Апельсин', '❌ Скрыть', '🥒 К овощам'])
def answer_fruits(message):
    fruit = message.text
    match fruit:
        case '🍎 Яблоко':
            response = "Яблоки полезны для сердца! ❤️"
        case '🍌 Банан':
            response = "Бананы содержат калий для мышц! 💪"
        case '🍊 Апельсин':
            response = "Апельсины укрепляют иммунитет! 🛡️"
        case '❌ Скрыть':
            bot.send_message(message.chat.id, "Клавиатура скрыта!", reply_markup=ReplyKeyboardRemove())
            return
        case '🥒 К овощам':
            confirm_markup = types.InlineKeyboardMarkup(row_width=2)
            conf_btn1 = types.InlineKeyboardButton('Да', callback_data='confirm_veg')
            conf_btn2 = types.InlineKeyboardButton('Нет', callback_data='cancel_veg')
            confirm_markup.add(conf_btn1, conf_btn2)
            bot.send_message(message.chat.id, 'Вы точно хоите перейти к овощам?', reply_markup=confirm_markup)
            return

    bot.send_message(message.chat.id, response)

@bot.callback_query_handler(func=lambda call: True)
def hundle_callback(call):
    if call.data == 'confirm_veg':
        bot.delete_message(call.message.chat.id, call.message.message_id)

        markup_veg = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        markup_veg.add(
            types.KeyboardButton('🥕 Морковь'),
            types.KeyboardButton('🥦 Брокколи'),
            types.KeyboardButton('🍅 Помидор'),
            types.KeyboardButton('🍎 К фруктам'),
            types.KeyboardButton('❌ Скрыть'),
        )
        bot.send_message(call.message.chat.id, 'Выберите овощ:', reply_markup=markup_veg)
    elif call.data == 'cancel_veg':
        bot.delete_message(call.message.chat.id, call.message.message_id)

        bot.send_message(call.message.chat.id, 'Остаемся с фруктами!')

@bot.message_handler(func=lambda message: message.text in ['🥕 Морковь','🥦 Брокколи','🍅 Помидор','🍎 К фруктам','❌ Скрыть'])
def answer_vegetables(message):
    veget = message.text
    match veget:
        case '🥕 Морковь':
            response = 'Морковь полезна для зрения! 👀'
        case '🥦 Брокколи':
            response = 'Брокколи богата витамином K! 💊'
        case '🍅 Помидор':
            response = 'Помидоры содержат ликопин! 🔴'
        case '🍎 К фруктам':
            bot.send_message(message.chat.id, 'Вернемся к фруктам!')
            time.sleep(1)
            bot.delete_message(message.chat.id, message.message_id)
            start_1(message)
        case '❌ Скрыть':
            bot.send_message(message.chat.id, "Клавиатура скрыта!", reply_markup=ReplyKeyboardRemove())
            return
    bot.send_message(message.chat.id, response)


bot.infinity_polling()