from .base_repository import BaseRepository

class ProductRepository(BaseRepository):
  def get_by_vendor(self, vendor_id):
    sql = "SELECT * FROM products WHERE vendor_id = %s"
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (vendor_id,))
        return cursor.fetchall()

  def add_product(self, vendor_id, name, price, stock, tags):
    t1, t2, t3 = (tags + [None] * 3)[:3]
    sql = """
      INSERT INTO products (vendor_id, name, listed_price, stock_quantity, tag1, tag2, tag3)
      VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (vendor_id, name, price, stock, t1, t2, t3))
        conn.commit()

  def search_by_tag(self, keyword):
    search_term = f"%{keyword}%"
    sql = """
      SELECT * FROM products 
      WHERE name LIKE %s OR tag1 LIKE %s OR tag2 LIKE %s OR tag3 LIKE %s
    """
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (search_term, keyword, keyword, keyword))
        return cursor.fetchall()

  def update_stock(self, cursor, product_id, quantity):
    sql = "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s"
    cursor.execute(sql, (quantity, product_id))