import pymysql
from models.customer import Customer
from config.database import Database


class CustomerRepository:
    """customer db operations"""

    def get_all(self) -> list[Customer]:
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM customers ORDER BY customer_id")
            rows = cursor.fetchall()
            return [Customer(**row) for row in rows]

    def create(self, customer: Customer) -> int:
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO customers (contact_number, shipping_address)
                VALUES (%s, %s)
            """, (customer.contact_number, customer.shipping_address))
            conn.commit()
            return cursor.lastrowid