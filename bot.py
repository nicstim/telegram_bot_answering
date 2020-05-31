import telebot
from telebot import types

admin = " Ваш  ID"

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands = ["get"])
def get(message): # Ваш telegram ID
    id = str(message.from_user.id)
    bot.send_message(id,f"Ваш ID\n{id}")


@bot.message_handler(commands = ["start"])
def start(message): # Приветствие
    bot.send_message(message.chat.id,f"""
Привет, {message.from_user.username} !
Задай мне вопрос.
    """)


@bot.message_handler(content_types = ["text","photo"])
def body(message):

    id = str(message.from_user.id)
    if id == admin:
        # Не реагируем на сообщения админа
        print("pass")
    else:
        feedback = types.InlineKeyboardMarkup(row_width = 1) # Создаем кнопки
        b1 = types.InlineKeyboardButton(text = "Ответить", callback_data = f"id{id}")
        feedback.add(b1)
        bot.forward_message(admin, message.chat.id, message.message_id) # пересылаем сообщение админу
        bot.send_message(admin,"Ответить?", reply_markup = feedback)


def reply_msg(message): # Отправка сообщения клиенту
    bot.forward_message(ID, message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data.startswith("id"):
        global ID
        ID = str(c.data.replace("id","")) # ID клиента
        s = bot.send_message(c.message.chat.id,"Отправьте фото или текст для ответа:")
        bot.register_next_step_handler(s,reply_msg) # Переходим в reply_msg



bot.skip_pending = True
bot.polling(none_stop=True, interval=0)





# https://github.com/nicstim
# t.me/nicstim
# 31.05.2020
