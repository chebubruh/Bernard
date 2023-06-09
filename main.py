from aiogram import *
import speech_to_text
import config
import openai
import json
import sql
import gpt
import os

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='К вашим услугам, сэр!')

    try:
        await sql.create_table(message.chat.id, message.chat.first_name.split()[
            0])  # Попытка создания таблицы, если она еще не существует
    except:
        await sql.table_clearing(message.chat.id)  # Очистка таблицы от предыдущих данных


@dp.message_handler(content_types=['text'])
async def chat(message: types.Message):
    m1 = await bot.send_message(chat_id=message.chat.id,
                                text='Обработка запроса...')  # Отправка сообщения о начале обработки запроса

    try:
        await sql.create_table(message.chat.id, message.chat.first_name.split()[
            0])  # Попытка создания таблицы, если она еще не существует
    except:
        pass

    answer = await gpt.gpt(message.chat.id, message.chat.first_name, message.text)

    if answer == "InvalidRequestError" or answer is None:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=m1.message_id,
                                    text='Упс, моя база данных переполнена. К сожалению мне придется стереть себе память, чтобы функицонировать дальше.')  # Редактирование сообщения
        await bot.send_message(chat_id=message.chat.id,
                               text='Пожалуйста, повторите свой запрос, но помните, что я не знаю, о чем мы говорили ранее.')  # Отправка сообщения
        await sql.table_clearing(message.chat.id)
    else:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=m1.message_id,
                                    text=f'{answer}')  # Редактирование сообщения с ответом


@dp.message_handler(content_types=['voice'])
async def voice(message: types.Message):
    m1 = await bot.send_message(chat_id=message.chat.id,
                                text='Обработка запроса...')  # Отправка сообщения о начале обработки запроса

    try:
        await sql.create_table(message.chat.id,
                               message.chat.first_name.split()[
                                   0])  # Попытка создания таблицы, если она еще не существует
    except:
        pass

    messages = [{"role": "system",
                 "content": "Ты интеллигентный, вежливый виртуальный помощник по имени Бернард"}]  # список для контекста

    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    folder_name = "voices"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    await bot.download_file(file_path, f"{folder_name}/audio.ogg")

    for token in config.TOKEN_GPT:
        openai.api_key = token

        try:
            content = speech_to_text.voice_converter()
            json_from_user = json.dumps(
                {"role": "user", "content": content})  # Преобразование текста пользователя в JSON
            await sql.insert_into_table_values(message.chat.id, message.chat.first_name.split()[0],
                                               json_from_user)  # Вставка сообщения пользователя в таблицу

            for i in await sql.select_data(message.chat.first_name.split()[0], message.chat.id):
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
            await sql.table_clearing(message.chat.id)  # Очистка таблицы от предыдущих данных
            await bot.edit_message_text(chat_id=message.chat.id, message_id=m1.message_id,
                                        text='Упс, моя база данных переполнена. К сожалению мне придется стереть себе память, чтобы функицонировать дальше.')  # Редактирование сообщения
            await bot.send_message(chat_id=message.chat.id,
                                   text='Пожалуйста, повторите свой запрос, но помните, что я не знаю, о чем мы говорили ранее.')  # Отправка сообщения
            break

        response = completion.choices[0].message.content  # Получение ответа от модели
        json_from_assistant = json.dumps({"role": "assistant", "content": response})  # Преобразование ответа в JSON
        await sql.insert_into_table_values(message.chat.id, message.chat.first_name.split()[0],
                                           json_from_assistant)  # Вставка ответа ассистента в таблицу
        await bot.edit_message_text(chat_id=message.chat.id, message_id=m1.message_id,
                                    text=f'{response}')  # Редактирование сообщения с ответом
        print(f'{messages}\n')
        break


executor.start_polling(dp, skip_updates=True)  # Запуск бота для прослушивания сообщений
