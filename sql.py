import config
from psycopg2 import *


def create_table(chat_id, first_name):
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(
            f'''CREATE TABLE "{chat_id}" (id serial PRIMARY KEY, {first_name.lower()} JSONB)''')


def table_clearing(chat_id):
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(f'''DELETE FROM "{chat_id}"''')


def insert_into_table_values(chat_id, first_name, values):
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(
            f'''INSERT INTO "{chat_id}" ({first_name.lower()}) VALUES (%s)''', (values,))


def select_data(first_name, chat_id):
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(f'''SELECT {first_name.lower()} FROM "{chat_id}"''')
        a = cur.fetchall()
    return a
