import pymysql
from pymysql.cursors import DictCursor

class Database:
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None or not cls._connection.open:
            cls._connection = pymysql.connect(
                host='localhost',
                user='root',
                password='764019',   # change to your MySQL password
                database='comp7640_ecommerce',
                charset='utf8mb4',
                cursorclass=DictCursor,
                autocommit=True
            )
        return cls._connection

    @classmethod
    def close(cls):
        if cls._connection and cls._connection.open:
            cls._connection.close()