from aiogram import *
import config
import sql
import gpt

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='К вашим услугам, сэр!')

    try:
        await sql.create_table(message.chat.id, message.chat.first_name.split()[
            0])  # Попытка создания таблицы, если она еще не существует
    except:
        # Очистка таблицы от предыдущих данных
        await sql.table_clearing(message.chat.id)


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


# Запуск бота для прослушивания сообщений
executor.start_polling(dp, skip_updates=True)
