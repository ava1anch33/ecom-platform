import pymysql
from models.order import Order, OrderStatus
from models.order_item import OrderItem
from config.database import Database


class OrderRepository:
    """order db operations"""

    def create_order(self, order: Order) -> int:
        """create new order"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO orders (customer_id, total_price, status)
                VALUES (%s, %s, %s)
            """, (order.customer_id, order.total_price, order.status.value))
            order_id = cursor.lastrowid
            conn.commit()
            return order_id

    def get_by_customer(self, customer_id: int) -> list[Order]:
        """get all orders of a customer, sorted by order_date desc"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM orders 
                WHERE customer_id = %s 
                ORDER BY order_date DESC
            """, (customer_id,))
            rows = cursor.fetchall()
            return [Order(**row) for row in rows]

    def update_status(self, order_id: int, status: OrderStatus):
        """update order status (Order Fulfillment)"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE orders 
                SET status = %s 
                WHERE order_id = %s AND status = 'PENDING'
            """, (status.value, order_id))
            conn.commit()

    def add_order_item(self, item: OrderItem):
        """add an item to an existing order (Order Modification)"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO order_items 
                (order_id, product_id, quantity, price_at_purchase)
                VALUES (%s, %s, %s, %s)
            """, (item.order_id, item.product_id, item.quantity, item.price_at_purchase))
            conn.commit()

    def remove_order_item(self, order_item_id: int):
        """remove an item from an existing order (Order Modification)"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM order_items WHERE order_item_id = %s", (order_item_id,))
            conn.commit()

    def cancel_order(self, order_id: int):
        """cancel an order (Order Cancellation) - only if it's still pending"""
        self.update_status(order_id, OrderStatus.CANCELLED)