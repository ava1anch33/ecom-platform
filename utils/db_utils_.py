import pymysql
from config import DB_CONFIG

class DBHelper:
  @staticmethod
  def get_connection():
    return pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)