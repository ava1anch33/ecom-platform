import pymysql
from models.vendor import Vendor
from config.database import Database


class VendorRepository:
    """vendor db operations"""

    def get_all(self) -> list[Vendor]:
        """1. show all vendors"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM vendors 
                ORDER BY business_name
            """)
            rows = cursor.fetchall()
            return [Vendor(**row) for row in rows]

    def create(self, vendor: Vendor) -> int:
        """2. Onboard new vendor"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO vendors (business_name, average_rating, geographical_presence)
                VALUES (%s, %s, %s)
            """, (vendor.business_name, vendor.average_rating, vendor.geographical_presence))
            conn.commit()
            return cursor.lastrowid