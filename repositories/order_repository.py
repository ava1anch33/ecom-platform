from .base_repository import BaseRepository

class OrderRepository(BaseRepository):
  def create_order_with_transaction(self, customer_id, items, vendor_amounts):
    with self._get_connection() as conn:
      conn.begin()
      try:
        with conn.cursor() as cursor:
          total_price = sum(amt for amt in vendor_amounts.values())
          cursor.execute(
            "INSERT INTO orders (customer_id, total_price, status) VALUES (%s, %s, 'PENDING')",
            (customer_id, total_price)
          )
          order_id = conn.insert_id()

          for p_id, qty, price in items:
            cursor.execute(
              "INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (%s, %s, %s, %s)",
              (order_id, p_id, qty, price)
            )
            cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s", (qty, p_id))

          for v_id, amount in vendor_amounts.items():
            cursor.execute(
              "INSERT INTO transactions (order_id, vendor_id, amount) VALUES (%s, %s, %s)",
              (order_id, v_id, amount)
            )
          
          conn.commit()
          return order_id
      except Exception as e:
        conn.rollback()
        raise e

  def update_status(self, order_id, status):
    sql = "UPDATE orders SET status = %s WHERE order_id = %s"
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (status, order_id))
        conn.commit()

  def get_order_details(self, order_id):
    sql = "SELECT * FROM orders WHERE order_id = %s"
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (order_id,))
        return cursor.fetchone()
  
  def get_order_items(self, order_id):
    """Get all products in an order with their quantities and purchase prices."""
    sql = "SELECT * FROM order_items WHERE order_id = %s"
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (order_id,))
        return cursor.fetchall()
      
  def remove_item_by_id(self, order_item_id, order_id, new_total):
        with self._get_connection() as conn:
            conn.begin()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM order_items WHERE order_item_id = %s", (order_item_id,))
                    cursor.execute("UPDATE orders SET total_price = %s WHERE order_id = %s", (new_total, order_id))
                    conn.commit()
                    return True
            except Exception as e:
                conn.rollback()
                raise e