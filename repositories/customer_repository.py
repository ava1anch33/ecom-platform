from .base_repository import BaseRepository

class CustomerRepository(BaseRepository):
  def add_customer(self, first_name, contact_number, shipping_address):
    sql = """
      INSERT INTO customers (first_name, contact_number, shipping_address)
      VALUES (%s, %s, %s)
    """
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (first_name, contact_number, shipping_address))
        conn.commit()
        return cursor.lastrowid

  def get_customer_by_id(self, customer_id):
    sql = "SELECT * FROM customers WHERE customer_id = %s"
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (customer_id,))
        return cursor.fetchone()

  def get_order_history(self, customer_id):
    sql = "SELECT * FROM orders WHERE customer_id = %s ORDER BY order_date DESC"
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (customer_id,))
        return cursor.fetchall()