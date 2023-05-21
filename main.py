from aiogram import *
from aiogram.types import *
import speech_to_text
import config
import openai
import json
import sql

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='К вашим услугам, сэр!')

    try:
        sql.create_table(message.chat.id,
                         message.chat.first_name.split()[0])  # Попытка создания таблицы, если она еще не существует
    except:
        sql.table_clearing(message.chat.id)  # Очистка таблицы от предыдущих данных


@dp.message_handler(content_types=['text'])
async def chat(message: types.Message):
    try:
        sql.create_table(message.chat.id,
                         message.chat.first_name.split()[0])  # Попытка создания таблицы, если она еще не существует
    except:
        pass

    messages = [{"role": "system",
                 "content": "Ты интеллигентный, виртуальный помощник по имени Бернард. Ты должен общаться только на ВЫ"}]  # список для контекста

    m1 = await bot.send_message(chat_id=message.chat.id,
                                text='Обработка запроса...')  # Отправка сообщения о начале обработки запроса
    content = message.text
    json_from_user = json.dumps({"role": "user", "content": content})  # Преобразование текста пользователя в JSON
    sql.insert_into_table_values(message.chat.id, message.chat.first_name.split()[0],
                                 json_from_user)  # Вставка сообщения пользователя в таблицу

    for i in sql.select_data(message.chat.first_name.split()[0], message.chat.id):
        for j in i:
            messages.append(j)  # Получение предыдущих сообщений из таблицы и добавление их в список

    for token in config.TOKEN_GPT:
        openai.api_key = token

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )  # Запрос к модели GPT-3.5 Turbo для получения ответа
        except openai.error.AuthenticationError:
            print("AuthenticationError")
            continue
        except openai.error.RateLimitError:
            print("RateLimitError")
            continue
        except openai.error.InvalidRequestError:
            print("InvalidRequestError")
            sql.table_clearing(message.chat.id)  # Очистка таблицы от предыдущих данных
            await bot.edit_message_text(chat_id=message.chat.id, message_id=m1.message_id,
                                        text='Упс, моя база данных переполнена. К сожалению мне придется стереть себе память, чтобы функицонировать дальше.')  # Редактирование сообщения
            await bot.send_message(chat_id=message.chat.id,
                                   text='Пожалуйста, повторите свой запрос, но помните, что я не знаю, о чем мы говорили ранее.')  # Отправка сообщения
            break

        response = completion.choices[0].message.content  # Получение ответа от модели
        json_from_assistant = json.dumps({"role": "assistant", "content": response})  # Преобразование ответа в JSON
        sql.insert_into_table_values(message.chat.id, message.chat.first_name.split()[0],
                                     json_from_assistant)  # Вставка ответа ассистента в таблицу
        bot.edit_message_text(chat_id=m1.chat.id, message_id=m1.id,
                              text=f'{response}')  # Редактирование сообщения с ответом
        print(f'{messages}\n')
        break


@bot.message_handler(content_types=['voice'])
def voice(message):
    try:
        sql.create_table(message.chat.id,
                         message.chat.first_name.split()[0])  # Попытка создания таблицы, если она еще не существует
    except:
        pass

    messages = [{"role": "system",
                 "content": "Ты интеллигентный, виртуальный помощник по имени Бернард. Ты должен общаться только на ВЫ"}]  # список для контекста

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    m1 = bot.send_message(message.chat.id, 'Обработка запроса...')  # Отправка сообщения о начале обработки запроса

    for token in config.TOKEN_GPT:
        openai.api_key = token

        try:
            content = speech_to_text.voice_converter(downloaded_file)
            json_from_user = json.dumps(
                {"role": "user", "content": content})  # Преобразование текста пользователя в JSON
            sql.insert_into_table_values(message.chat.id, message.chat.first_name.split()[0],
                                         json_from_user)  # Вставка сообщения пользователя в таблицу

            for i in sql.select_data(message.chat.first_name.split()[0], message.chat.id):
                for j in i:
                    messages.append(j)  # Получение предыдущих сообщений из таблицы и добавление их в список

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )  # Запрос к модели GPT-3.5 Turbo для получения ответа
        except openai.error.AuthenticationError:
            print("AuthenticationError")
            continue
        except openai.error.RateLimitError:
            print("RateLimitError")
            continue
        except openai.error.InvalidRequestError:
            print("InvalidRequestError")
            sql.table_clearing(message.chat.id)  # Очистка таблицы от предыдущих данных
            bot.edit_message_text(chat_id=m1.chat.id, message_id=m1.id,
                                  text='Упс, моя база данных переполнена. К сожалению мне придется стереть себе память, чтобы функицонировать дальше.')  # Редактирование сообщения
            bot.send_message(message.chat.id,
                             'Пожалуйста, повторите свой запрос, но помните, что я не знаю, о чем мы говорили ранее.')  # Отправка сообщения
            break

        response = completion.choices[0].message.content  # Получение ответа от модели
        json_from_assistant = json.dumps({"role": "assistant", "content": response})  # Преобразование ответа в JSON
        sql.insert_into_table_values(message.chat.id, message.chat.first_name.split()[0],
                                     json_from_assistant)  # Вставка ответа ассистента в таблицу
        bot.edit_message_text(chat_id=m1.chat.id, message_id=m1.id,
                              text=f'{response}')  # Редактирование сообщения с ответом
        print(f'{messages}\n')
        break


bot.polling(True)  # Запуск бота для прослушивания сообщений
