from .base_repository import BaseRepository

class VendorRepository(BaseRepository):
  def list_all_vendors(self):
    sql = "SELECT * FROM vendors"
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()

  def onboard_new_vendor(self, business_name, geographical_presence):
    sql = """
      INSERT INTO vendors (business_name, geographical_presence)
      VALUES (%s, %s)
    """
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        try:
          cursor.execute(sql, (business_name, geographical_presence))
          conn.commit()
          return cursor.lastrowid
        except Exception as e:
          print(f"Error onboarding vendor: {e}")
          return None