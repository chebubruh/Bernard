import config
from psycopg2 import *
from psycopg2.extensions import AsIs


def create_table(chat_id, first_name):
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(
            '''CREATE TABLE "%s" (id serial PRIMARY KEY, %s JSONB)''', (AsIs(chat_id), AsIs(first_name.lower())))


def table_clearing(chat_id):
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute('''DELETE FROM "%s"''', (chat_id,))


def insert_into_table_values(chat_id, first_name, values):
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(
            '''INSERT INTO "%s" ("%s") VALUES (%s)''', (AsIs(chat_id), AsIs(first_name.lower()), values))


def select_data(first_name, chat_id):
    with connect(user=config.user, password=config.password, host=config.host, database=config.database,
                 port=config.port) as db:
        cur = db.cursor()
        cur.execute(f'''SELECT %s FROM "%s" ORDER BY id''', (AsIs(first_name.lower()), AsIs(chat_id)))
        a = cur.fetchall()
    return a
