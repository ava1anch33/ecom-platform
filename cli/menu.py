from cli.handlers import (
    show_vendors, add_vendor,
    show_products_by_vendor, add_product,
    search_products_by_tag,
    purchase_product,
    show_customer_orders, modify_order
)
import sys


def show_main_menu():
    """COMP7640 Multi-Vendor E-commerce Platform CLI Main Menu"""
    while True:
        print("\n" + "="*60)
        print("COMP7640 Multi Vendor Platform（Python CLI）")
        print("="*60)
        print("1. Show All Vendors")
        print("2. Create new Vendor")
        print("3. Show Product By Vendor")
        print("4. Create Product")
        print("5. Product Discovery")
        print("6. Product Purchase")
        print("7. Order Modification")
        print("0. !!Exit!!")
        print("="*60)

        choice = input("\n请输入选项 (0-7): ").strip()

        if choice == '1':
            show_vendors()
        elif choice == '2':
            add_vendor()
        elif choice == '3':
            show_products_by_vendor()
        elif choice == '4':
            add_product()
        elif choice == '5':
            search_products_by_tag()
        elif choice == '6':
            purchase_product()
        elif choice == '7':
            modify_order()
        elif choice == '0':
            print("\nThanks For Using COMP7640 Multi Vendor Platform CLI. Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please enter a number between 0 and 7.")