from telebot import *
import config
import openai
import json
import time
import sql

bot = TeleBot(config.TOKEN)
openai.api_key = config.TOKEN_GPT


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Плотный салам')

    try:
        sql.create_table(message.chat.id, message.chat.first_name)
    except:
        pass

    sql.table_clearing(message.chat.id)


@bot.message_handler(content_types=['text'])
def chat(message):
    try:
        sql.create_table(message.chat.id, message.chat.first_name)
    except:
        pass

    messages = [{"role": "system",
                 "content": "Ты - виртуальный помощник по имени Бернард. Ты должен общаться с собеседником на ВЫ, а не на ТЫ"}]
    m1 = bot.send_message(message.chat.id, 'Обработка запроса...')
    content = message.text
    json_from_user = json.dumps({"role": "user", "content": content})
    sql.insert_into_table_values(message.chat.id, message.chat.first_name, json_from_user)

    for i in sql.select_data(message.chat.first_name, message.chat.id):
        for j in i:
            messages.append(j)
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        response = completion.choices[0].message.content
        json_from_assistant = json.dumps({"role": "assistant", "content": response})
        sql.insert_into_table_values(message.chat.id, message.chat.first_name, json_from_assistant)
        bot.edit_message_text(chat_id=m1.chat.id, message_id=m1.id, text=f'{response}')


    except openai.error.RateLimitError:
        bot.edit_message_text(chat_id=m1.chat.id, message_id=m1.id,
                              text='Я упал, подождите пока я не сообщу вам о своей готовности')
        time.sleep(20)
        bot.send_message(message.chat.id, 'Все, я поднялся, повторите свой вопрос')

    except openai.error.InvalidRequestError:
        sql.table_clearing(message.chat.id)

        bot.edit_message_text(chat_id=m1.chat.id, message_id=m1.id,
                              text='Упс, моя база данных переполнена. К сожалению мне придется стереть себе память, чтобы функицонировать дальше')
        reload = bot.send_message(message.chat.id, 'Перезагрузка: <b>0%</b>', parse_mode='HTML')
        time.sleep(0.2)
        bot.edit_message_text(chat_id=reload.chat.id, message_id=reload.id,
                              text='Перезагрузка: <b>20%</b>', parse_mode='HTML')
        time.sleep(0.2)
        bot.edit_message_text(chat_id=reload.chat.id, message_id=reload.id,
                              text='Перезагрузка: <b>40%</b>', parse_mode='HTML')
        time.sleep(0.2)
        bot.edit_message_text(chat_id=reload.chat.id, message_id=reload.id,
                              text='Перезагрузка: <b>60%</b>', parse_mode='HTML')
        time.sleep(0.2)
        bot.edit_message_text(chat_id=reload.chat.id, message_id=reload.id,
                              text='Перезагрузка: <b>80%</b>', parse_mode='HTML')
        time.sleep(0.2)
        bot.edit_message_text(chat_id=reload.chat.id, message_id=reload.id,
                              text='Перезагрузка: <b>100%</b>', parse_mode='HTML')
        time.sleep(0.2)
        bot.edit_message_text(chat_id=reload.chat.id, message_id=reload.id,
                              text='Здравствуйте, как я могу вам помочь?')

    except:
        sql.table_clearing(message.chat.id)

        bot.edit_message_text(chat_id=m1.chat.id, message_id=m1.id,
                              text='Произошла какая-то неизвестная ошибка, откатываюсь к заводским настройкам')

    print(f'{messages}\n')


bot.polling(True)
