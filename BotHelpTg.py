from telebot import types

import telebot

TO_CHAT_ID = #id юзверя, кому будут приходить сообщения

bot = telebot.TeleBot('') #токен бота

requests_queue = []

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Здравствуйте!, {0.first_name}!\n Пиши сюда заебал".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')
    bot.register_next_step_handler(message, help_bot)


# Функция, отправляющая вопрос от пользователя в чат поддержки
def help_bot(message):
    requests_queue.append((message.message_id, message.chat.id))
    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
    markup_inline = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(text='Ответить', callback_data=f'answer{message.chat.id}')
    ]])
    bot.send_message(TO_CHAT_ID, f"Действие:", reply_markup=markup_inline)
    bot.register_next_step_handler(message, help_bot)
    print(str(message.from_user) + ' пишет: ' + message.text)
    with open("C:/Users/Толик-еболик/Desktop/TgbotLog/log.txt", "a", errors='ignore') as log:
        log.write((str(message.from_user)) + ' Написал: ' + message.text + '\n')


@bot.message_handler(commands=["requests"], func=lambda m: int(m.chat.id) == int(TO_CHAT_ID))
def all_messages(message):
    bot.send_message(message.chat.id, "Доступные запросы:")
    for i, req in enumerate(requests_queue):
        bot.forward_message(TO_CHAT_ID, req[1], req[0])
        markup_inline = types.InlineKeyboardMarkup([[
            types.InlineKeyboardButton(text='Ответить', callback_data=f'answer{req[1]}')
        ]])
        bot.send_message(message.chat.id, f"Действие:", reply_markup=markup_inline)
    print(str(message.from_user) + ' пишет: ' + message.text)
    with open("C:/Users/Толик-еболик/Desktop/TgbotLog/log.txt", "a", errors='ignore') as log:
        log.write((str(message.from_user)) + ' Написал: ' + message.text + '\n')

def send_answer(message: types.Message, call, chat_id):
    bot.send_message(call.message.chat.id, "Ответ отправлен!")
    bot.send_message(chat_id, message.text)
    for i, req in enumerate(requests_queue):
        if int(req[1]) == int(chat_id):
            del requests_queue[i]
    print(str(message.from_user) + ' пишет: ' + message.text)
    with open("C:/Users/Толик-еболик/Desktop/TgbotLog/log.txt", "a", errors='ignore') as log:
        log.write((str(message.from_user)) + ' Написал: ' + message.text + '\n')


@bot.callback_query_handler(func=lambda call: True)
def answer_callback(call: types.CallbackQuery):
    if call.data.startswith("answer"):
        chat_id = int(call.data[6:])

        bot.send_message(call.message.chat.id, "Отправьте ответ на запрос")
        bot.register_next_step_handler(call.message, lambda msg: send_answer(msg, call, chat_id))



bot.infinity_polling()
bot.polling()
