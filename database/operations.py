from typing import List

from .connection import UseDatabase

from mysql.connector import connect

from flask import current_app


def select(db_config: dict, sql: str) -> List:
    result = []
    with UseDatabase(db_config) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))

    return result


def insert(sql: str):
    with connect(
            host="localhost",
            user="root",
            password="qwerty",
            database="internet"
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()

def exists(sql: str):
    with connect(
            host="localhost",
            user="root",
            password="qwerty",
            database="internet"
    ) as connection:
        with connection.cursor() as cursor:
            res = cursor.execute(sql)
            connection.commit()
        return res

def call_proc(proc_name: str, *args):
    with connect(
            host="localhost",
            user="root",
            password="qwerty",
            database="internet"
    ) as connection:
        with connection.cursor() as cursor:
            if cursor is None:
                raise ValueError('Курсор не создан')
            param_list = []
            for arg in args:
                param_list.append(arg)
            cursor.callproc(proc_name, param_list)
            res = cursor.callproc(proc_name, param_list)
            connection.commit()
        return res


def delete(sql: str):
    with connect(
            host="localhost",
            user="root",
            password="qwerty",
            database="internet"
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()


def check(sql: str):
    with connect(
            host="localhost",
            user="root",
            password="qwerty",
            database="internet"
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
