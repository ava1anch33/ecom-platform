import pymysql
from models.transaction import Transaction
from config.database import Database


class TransactionRepository:
    """transaction db operations"""

    def create(self, transaction: Transaction) -> int:
        """create new transaction record"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO transactions (order_id, vendor_id, amount)
                VALUES (%s, %s, %s)
            """, (transaction.order_id, transaction.vendor_id, transaction.amount))
            conn.commit()
            return cursor.lastrowid

    def get_by_order(self, order_id: int) -> list[Transaction]:
        """get all transactions related to an order (for order history and refunds)"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM transactions 
                WHERE order_id = %s
            """, (order_id,))
            rows = cursor.fetchall()
            return [Transaction(**row) for row in rows]