from .base_repository import BaseRepository

class TransactionRepository(BaseRepository):
  def get_transactions_by_order(self, order_id):
    sql = "SELECT * FROM transactions WHERE order_id = %s"
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (order_id,))
        return cursor.fetchall()

  def get_vendor_earnings(self, vendor_id):
    sql = "SELECT SUM(amount) as total_earnings FROM transactions WHERE vendor_id = %s"
    with self._get_connection() as conn:
      with conn.cursor() as cursor:
        cursor.execute(sql, (vendor_id,))
        result = cursor.fetchone()
        return result['total_earnings'] if result['total_earnings'] else 0