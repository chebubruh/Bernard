import config
from asyncpg import *
import json


async def create_table(chat_id, first_name):
    conn = await connect(user=config.user, password=config.password, host=config.host, database=config.database,
                         port=config.port)
    try:
        await conn.execute(f'''CREATE TABLE "{chat_id}" (id SERIAL PRIMARY KEY, _{first_name.lower()} JSONB)''')
    except Exception as ex:
        print(ex)
    finally:
        await conn.close()


async def table_clearing(chat_id):
    conn = await connect(user=config.user, password=config.password, host=config.host, database=config.database,
                         port=config.port)
    try:
        await conn.execute(f'''DELETE FROM "{chat_id}"''')
    except Exception as ex:
        print(ex)
    finally:
        await conn.close()


async def insert_into_table_values(chat_id, first_name, values):
    conn = await connect(user=config.user, password=config.password, host=config.host, database=config.database,
                         port=config.port)
    try:
        await conn.execute(f'''INSERT INTO "{chat_id}" (_{first_name.lower()}) VALUES ($1)''', values)
    except Exception as ex:
        print(ex)
    finally:
        await conn.close()


async def select_data(first_name, chat_id):
    conn = await connect(user=config.user, password=config.password, host=config.host, database=config.database,
                         port=config.port)
    result = list()
    try:
        r = await conn.fetch(f'''SELECT _{first_name.lower()} FROM "{chat_id}" ORDER BY id''')

        for i in r:
            for j in i:
                dictionary = json.loads(j)
                tuple_ = (dictionary,)
                result.append(tuple_)
    except Exception as ex:
        print(ex)
    finally:
        await conn.close()
        return result

# БД В СИНХРОННОМ РЕЖИМЕ-------------------------------------------

# from psycopg2 import *
# from psycopg2.extensions import AsIs

# def create_table(chat_id, first_name):
#     with connect(user=config.user, password=config.password, host=config.host, database=config.database,
#                  port=config.port) as db:
#         cur = db.cursor()
#         cur.execute(
#             '''CREATE TABLE "%s" (id serial PRIMARY KEY, %s JSONB)''', (AsIs(chat_id), AsIs(first_name.lower())))
#
#
# def table_clearing(chat_id):
#     with connect(user=config.user, password=config.password, host=config.host, database=config.database,
#                  port=config.port) as db:
#         cur = db.cursor()
#         cur.execute('''DELETE FROM "%s"''', (chat_id,))
#
#
# def insert_into_table_values(chat_id, first_name, values):
#     with connect(user=config.user, password=config.password, host=config.host, database=config.database,
#                  port=config.port) as db:
#         cur = db.cursor()
#         cur.execute(
#             '''INSERT INTO "%s" ("%s") VALUES (%s)''', (AsIs(chat_id), AsIs(first_name.lower()), values))
#
#
# def select_data(first_name, chat_id):
#     with connect(user=config.user, password=config.password, host=config.host, database=config.database,
#                  port=config.port) as db:
#         cur = db.cursor()
#         cur.execute(f'''SELECT %s FROM "%s" ORDER BY id''', (AsIs(first_name.lower()), AsIs(chat_id)))
#         a = cur.fetchall()
#     return a
