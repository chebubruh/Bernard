import openai_async
import config
import openai
import json
import sql


async def gpt(chat_id, first_name, content):  # content должен быть message.text
    try:
        await sql.create_table(chat_id, first_name.split()[0])  # Попытка создания таблицы, если она еще не существует
    except:
        pass

    messages = [{"role": "system",
                 "content": "Ты интеллигентный, вежливый виртуальный помощник по имени Бернард"}]  # список для контекста

    json_from_user = json.dumps({"role": "user", "content": content})  # Преобразование текста пользователя в JSON

    await sql.insert_into_table_values(chat_id, first_name.split()[0],
                                       json_from_user)  # Вставка сообщения пользователя в таблицу

    for i in await sql.select_data(first_name.split()[0], chat_id):
        for j in i:
            messages.append(j)  # Получение предыдущих сообщений из таблицы и добавление их в список

    for token in config.TOKEN_GPT:
        try:
            completion = await openai_async.chat_complete(
                token,
                timeout=None,
                payload={
                    "model": "gpt-3.5-turbo",
                    "messages": messages,
                },
            )  # Запрос к модели GPT-3.5 Turbo для получения ответа
            response = completion.json()['choices'][0]['message']['content']  # Получение ответа от модели
        except openai.error.AuthenticationError:
            print("AuthenticationError")
            continue
        except openai.error.RateLimitError:
            print("RateLimitError")
            continue
        except KeyError:
            print("KeyError: 'choices'")
            continue
        except openai.error.InvalidRequestError:
            print("InvalidRequestError")
            await sql.table_clearing(chat_id)  # Очистка таблицы от предыдущих данных
            return "InvalidRequestError"
            break

        json_from_assistant = json.dumps({"role": "assistant", "content": response})  # Преобразование ответа в JSON

        await sql.insert_into_table_values(chat_id, first_name.split()[0],
                                           json_from_assistant)  # Вставка ответа ассистента в таблицу
        print(f'{messages}\n')
        return response
