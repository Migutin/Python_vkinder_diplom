import psycopg2
from token_date import *

connect = psycopg2.connect(database="vkinderDB", user="postgres", password="33851")

connect.autocommit = True

dict_select = []

def create_users_tab_viewed():
    """Создание таблицы просмотренные user"""
    with connect.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS seen_users(
            id serial,
            vk_id varchar(50) PRIMARY KEY);"""
        )
    print("Создана таблица просмотренные user")

def drop_users_tab_viewed():
    """Удаление таблицы просмотренных user"""
    with connect.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS seen_users CASCADE;"""
        )
        print('Удалена таблица просмотренных user')

def insert_users_tab_viewed(vk_id, offset):
    """Добавление данных в таблицу просмотренных user"""
    with connect.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO seen_users (vk_id) 
            VALUES ('{vk_id}')
            OFFSET '{offset}';"""
        )

def select (offset):
    """Определение непросмотренного user """
    with connect.cursor() as cursor:
        cursor.execute(
            f"""SELECT  su.vk_id
                        FROM seen_users AS su;"""
        )
        return cursor.fetchall()

def select_id_database(offset):
    for id in select (offset):
        if id[0] not in dict_select:
            dict_select.append(id[0])
        else:
            break
    return dict_select

def database():
    create_users_tab_viewed()