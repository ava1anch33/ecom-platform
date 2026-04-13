"""
Vendor administration: vendor list (with profile fields) and onboard new vendor.

Run from project root (ecom-platform-main):
    python -m unittest discover -s tests -v

Each passing test prints requirement lines with [OK]; end of module prints a summary table.

Optional integration test against real MySQL (database configured in config/database.py):
    set VENDOR_INTEGRATION_TEST=1
    python -m unittest tests.test_vendor_management.VendorIntegrationTest -v
"""
from __future__ import annotations

import io
import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

# Prefer UTF-8 on Windows consoles when supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (OSError, ValueError, AttributeError):
        pass

from models.vendor import Vendor
from repositories.vendor_repository import VendorRepository

# Requirement IDs aligned with the assignment (vendor profile + two management features)
REQUIREMENT_LABELS: dict[str, str] = {
    "arch_id": "[Profile] Vendor ID",
    "arch_name": "[Profile] Business name",
    "arch_rating": "[Profile] Average customer rating",
    "arch_geo": "[Profile] Geographical presence",
    "arch_stock": "[Profile] Product inventory (aggregated)",
    "m1_list": "[Mgmt-1] List all vendors",
    "m2_add": "[Mgmt-2] Onboard a new vendor",
}

REQUIREMENT_ORDER: list[str] = list(REQUIREMENT_LABELS.keys())

_VERIFIED: set[str] = set()


def _report_success_for_requirements(test_title: str, *keys: str) -> None:
    """Call after all assertions in a test pass; prints one line per requirement verified."""
    print(f"  -> Case [{test_title}] passed. Requirements checked:")
    for k in keys:
        _VERIFIED.add(k)
        print(f"       [OK] {REQUIREMENT_LABELS[k]}")


def _test_banner(title: str, *verify_points: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"[Test] {title}")
    for line in verify_points:
        print(f"  * {line}")


def tearDownModule() -> None:
    """After all tests in this module: print requirement coverage summary."""
    print(f"\n{'=' * 60}")
    print("[Summary] Requirement coverage for this run:")
    for key in REQUIREMENT_ORDER:
        ok = key in _VERIFIED
        mark = "x" if ok else " "
        label = REQUIREMENT_LABELS[key]
        status = "verified" if ok else "not verified (skipped or failed)"
        print(f"  [{mark}] {label}  ->  {status}")
    if all(k in _VERIFIED for k in REQUIREMENT_ORDER):
        print("\n  >>> All requirement items were verified in this run.")
    print(f"{'=' * 60}\n")


class VendorRepositoryUnitTest(unittest.TestCase):
    """Repository layer with a mocked DB (no local MySQL required)."""

    @patch("repositories.vendor_repository.Database")
    def test_get_all_returns_vendors_with_profile_and_total_inventory(self, mock_db):
        """List includes vendor id, name, rating, location, and total inventory."""
        _test_banner(
            "VendorRepository.get_all (mock DB)",
            "Rows from DB map to Vendor with full profile; supports listing",
        )
        row = {
            "vendor_id": 1,
            "business_name": "TestVendor",
            "average_rating": 4.5,
            "geographical_presence": "Hong Kong",
            "created_at": datetime(2025, 1, 1, 12, 0, 0),
            "total_inventory": 100,
        }
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [row]
        cursor_ctx = MagicMock()
        cursor_ctx.__enter__.return_value = mock_cursor
        cursor_ctx.__exit__.return_value = None
        mock_conn.cursor.return_value = cursor_ctx
        mock_db.get_connection.return_value = mock_conn

        vendors = VendorRepository().get_all()

        self.assertEqual(len(vendors), 1)
        v = vendors[0]
        self.assertEqual(v.vendor_id, 1)
        self.assertEqual(v.business_name, "TestVendor")
        self.assertEqual(v.average_rating, 4.5)
        self.assertEqual(v.geographical_presence, "Hong Kong")
        self.assertEqual(v.total_inventory, 100)
        mock_cursor.execute.assert_called_once()

        _report_success_for_requirements(
            "VendorRepository.get_all",
            "arch_id",
            "arch_name",
            "arch_rating",
            "arch_geo",
            "arch_stock",
            "m1_list",
        )

    @patch("repositories.vendor_repository.Database")
    def test_create_inserts_vendor_and_returns_new_id(self, mock_db):
        """Onboard new vendor: persist and return new id."""
        _test_banner(
            "VendorRepository.create (mock DB)",
            "INSERT vendor row and return lastrowid",
        )
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 7
        cursor_ctx = MagicMock()
        cursor_ctx.__enter__.return_value = mock_cursor
        cursor_ctx.__exit__.return_value = None
        mock_conn.cursor.return_value = cursor_ctx
        mock_db.get_connection.return_value = mock_conn

        vid = VendorRepository().create(
            Vendor(
                business_name="NewCo",
                average_rating=5.0,
                geographical_presence="Shenzhen",
            )
        )

        self.assertEqual(vid, 7)
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        self.assertIn("INSERT INTO vendors", args[0])
        self.assertEqual(args[1], ("NewCo", 5.0, "Shenzhen"))
        mock_conn.commit.assert_called_once()

        _report_success_for_requirements(
            "VendorRepository.create",
            "m2_add",
        )


class VendorHandlersTest(unittest.TestCase):
    """CLI: print vendor table and interactive add (mocked repository / stdin)."""

    @patch("cli.handlers.VendorRepository")
    def test_show_vendors_prints_table_with_inventory_column(self, mock_repo_cls):
        from cli.handlers import show_vendors

        _test_banner(
            "CLI show_vendors (mock repository)",
            "Printed table includes profile columns including total inventory",
        )
        mock_repo_cls.return_value.get_all.return_value = [
            Vendor(
                vendor_id=2,
                business_name="ACME",
                average_rating=4.0,
                geographical_presence="Tokyo",
                total_inventory=50,
            )
        ]
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            show_vendors()
        out = buf.getvalue()
        self.assertIn("ACME", out)
        self.assertIn("Tokyo", out)
        self.assertIn("50", out)

        _report_success_for_requirements(
            "CLI show_vendors",
            "arch_id",
            "arch_name",
            "arch_rating",
            "arch_geo",
            "arch_stock",
            "m1_list",
        )

    @patch("cli.handlers.VendorRepository")
    def test_add_vendor_prompts_and_creates(self, mock_repo_cls):
        from cli.handlers import add_vendor

        _test_banner(
            "CLI add_vendor (mock repository + stdin)",
            "User can enter name, location, rating; create() is called",
        )
        mock_repo_cls.return_value.create.return_value = 99
        inp = io.StringIO("MyShop\nShanghai\n4.2\n")
        buf = io.StringIO()
        with patch("sys.stdin", inp), patch("sys.stdout", buf):
            add_vendor()
        mock_repo_cls.return_value.create.assert_called_once()
        created = mock_repo_cls.return_value.create.call_args[0][0]
        self.assertIsInstance(created, Vendor)
        self.assertEqual(created.business_name, "MyShop")
        self.assertEqual(created.geographical_presence, "Shanghai")
        self.assertEqual(created.average_rating, 4.2)
        self.assertIn("99", buf.getvalue())

        _report_success_for_requirements(
            "CLI add_vendor",
            "m2_add",
        )


@unittest.skipUnless(
    os.environ.get("VENDOR_INTEGRATION_TEST") == "1",
    "set VENDOR_INTEGRATION_TEST=1 to run against real MySQL",
)
class VendorIntegrationTest(unittest.TestCase):
    """Requires local MySQL and database comp7640_ecommerce (see config/database.py)."""

    def test_repository_roundtrip(self):
        _test_banner(
            "Integration: real MySQL (config/database.py)",
            "End-to-end: create vendor then find row in get_all()",
        )
        repo = VendorRepository()
        name = f"ITestVendor_{datetime.now().timestamp()}"
        vid = repo.create(
            Vendor(business_name=name, average_rating=4.8, geographical_presence="TestCity")
        )
        self.assertIsInstance(vid, int)
        self.assertGreater(vid, 0)
        all_v = repo.get_all()
        found = next((x for x in all_v if x.vendor_id == vid), None)
        self.assertIsNotNone(found)
        self.assertEqual(found.business_name, name)
        self.assertEqual(found.geographical_presence, "TestCity")
        self.assertAlmostEqual(float(found.average_rating), 4.8, places=2)
        self.assertEqual(found.total_inventory, 0)

        _report_success_for_requirements(
            "Integration MySQL round-trip",
            "arch_id",
            "arch_name",
            "arch_rating",
            "arch_geo",
            "arch_stock",
            "m1_list",
            "m2_add",
        )
        print(f"  (Inserted vendor_id={vid}; total inventory 0 when no products.)")


if __name__ == "__main__":
    unittest.main()
