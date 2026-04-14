import pymysql

class BaseRepository:
  def __init__(self, db_config):
    self.db_config = db_config

  def _get_connection(self):
    return pymysql.connect(
      **self.db_config,
      cursorclass=pymysql.cursors.DictCursor
    )