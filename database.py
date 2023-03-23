import psycopg2
from token_date import *

connect = psycopg2.connect(database="vkinderDB", user="postgres", password="33851")

connect.autocommit = True


def create_users_tab():
    """Создание таблицы user"""
    with connect.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id serial,
                first_name varchar(50) NOT NULL,
                last_name varchar(30) NOT NULL,
                vk_id varchar(20) NOT NULL PRIMARY KEY,
                vk_link varchar(50),
                bdate varchar(30));"""
        )
    print("Создана таблица user")

def drop_users_tab():
    """Удаление таблицы user"""
    with connect.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS users CASCADE;"""
        )
        print('Удалена таблица user')

def insert_users_tab(first_name, last_name, vk_id, vk_link,bdate):
    """Добавление данных в таблицу user"""
    with connect.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO users (first_name, last_name, vk_id, vk_link,bdate) 
            VALUES ('{first_name}', '{last_name}', '{vk_id}', '{vk_link}', '{bdate}');"""
        )

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
            f"""SELECT  u.first_name,
                        u.last_name,
                        u.vk_id,
                        u.vk_link,
                        u.bdate,
                        su.vk_id
                        FROM users AS u
                        LEFT JOIN seen_users AS su 
                        ON u.vk_id = su.vk_id
                        WHERE su.vk_id IS NULL
                        OFFSET '{offset}';"""
        )
        return cursor.fetchone()

def database():
    drop_users_tab()
    drop_users_tab_viewed()
    create_users_tab()
    create_users_tab_viewed()