from models.vendor import Vendor
from config.database import Database


class VendorRepository:
    """vendor db operations"""

    def get_all(self) -> list[Vendor]:
        """1. show all vendors (includes aggregate product stock per vendor)"""
        conn = Database.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    v.vendor_id,
                    v.business_name,
                    v.average_rating,
                    v.geographical_presence,
                    v.created_at,
                    COALESCE(SUM(p.stock_quantity), 0) AS total_inventory
                FROM vendors v
                LEFT JOIN products p ON p.vendor_id = v.vendor_id
                GROUP BY
                    v.vendor_id,
                    v.business_name,
                    v.average_rating,
                    v.geographical_presence,
                    v.created_at
                ORDER BY v.business_name
            """)
            rows = cursor.fetchall()
            out: list[Vendor] = []
            for row in rows:
                r = dict(row)
                r["total_inventory"] = int(r["total_inventory"])
                out.append(Vendor(**r))
            return out

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
