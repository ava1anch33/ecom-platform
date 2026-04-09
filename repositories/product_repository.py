import pymysql
from models.product import Product
from config.database import Database


class ProductRepository:
    """product db operations"""

    def get_by_vendor(self, vendor_id: int) -> list[Product]:
        """1. get all products of a vendor"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM products 
                WHERE vendor_id = %s
                ORDER BY name
            """, (vendor_id,))
            rows = cursor.fetchall()
            return [Product(**row) for row in rows]

    def create(self, product: Product) -> int:
        """2. create new product"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO products 
                (vendor_id, name, listed_price, stock_quantity, tag1, tag2, tag3)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (product.vendor_id, product.name, product.listed_price,
                  product.stock_quantity, product.tag1, product.tag2, product.tag3))
            conn.commit()
            return cursor.lastrowid

    def search_by_tag(self, keyword: str) -> list[Product]:
        """Product Discovery: search products by name or tags"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM products 
                WHERE name LIKE %s 
                   OR tag1 LIKE %s 
                   OR tag2 LIKE %s 
                   OR tag3 LIKE %s
                ORDER BY name
            """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
            rows = cursor.fetchall()
            return [Product(**row) for row in rows]
    
    def update_stock(self, product_id: int, new_quantity: int):
        """Update stock quantity after purchase"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE products 
                SET stock_quantity = %s 
                WHERE product_id = %s
            """, (new_quantity, product_id))
            conn.commit()
        
