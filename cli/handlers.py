from repositories.vendor_repository import VendorRepository
from repositories.product_repository import ProductRepository
from repositories.customer_repository import CustomerRepository
from repositories.order_repository import OrderRepository
from repositories.transaction_repository import TransactionRepository
from services.product_service import ProductService
from models.vendor import Vendor
from models.product import Product
from models.customer import Customer
from models.order import Order, OrderStatus
from models.order_item import OrderItem
from models.transaction import Transaction
from tabulate import tabulate
from datetime import datetime


# ==================== Vendor Administration ====================
def show_vendors():
    vendors = VendorRepository().get_all()
    if not vendors:
        print("暂无商户")
        return
    table = [[v.vendor_id, v.business_name, v.average_rating, v.geographical_presence] 
             for v in vendors]
    print(tabulate(table, headers=["ID", "商户名称", "平均评分", "地理位置"], tablefmt="grid"))


def add_vendor():
    print("\n=== 新增商户 ===")
    name = input("请输入商户名称: ").strip()
    location = input("请输入地理位置 (e.g. Tokyo): ").strip()
    rating = float(input("请输入初始评分 (0-5，默认5.0): ") or 5.0)
    
    vendor = Vendor(business_name=name, average_rating=rating, geographical_presence=location)
    vendor_id = VendorRepository().create(vendor)
    print(f"✅ 商户新增成功！ID = {vendor_id}")


# ==================== Product Catalog Management ====================
def show_products_by_vendor():
    show_vendors()
    vendor_id = int(input("\n请输入要查看的商户 ID: "))
    products = ProductRepository().get_by_vendor(vendor_id)
    if not products:
        print("该商户暂无商品")
        return
    table = [[p.product_id, p.name, p.listed_price, p.stock_quantity, ", ".join(p.get_tags())] 
             for p in products]
    print(tabulate(table, headers=["ID", "商品名称", "价格", "库存", "Tags"], tablefmt="grid"))


def add_product():
    show_vendors()
    vendor_id = int(input("\n请输入商户 ID: "))
    print("\n=== 新增商品 ===")
    name = input("商品名称: ").strip()
    price = float(input("价格: "))
    stock = int(input("库存数量: "))
    tag1 = input("Tag1 (可空): ").strip() or None
    tag2 = input("Tag2 (可空): ").strip() or None
    tag3 = input("Tag3 (可空): ").strip() or None
    
    product = Product(vendor_id=vendor_id, name=name, listed_price=price, 
                      stock_quantity=stock, tag1=tag1, tag2=tag2, tag3=tag3)
    product_id = ProductRepository().create(product)
    print(f"✅ 商品新增成功！ID = {product_id}")


# ==================== Product Discovery ====================
def search_products_by_tag():
    keyword = input("\n请输入搜索关键词 (标签或商品名称): ").strip()
    products = ProductRepository().search_by_tag(keyword)
    if not products:
        print("没有找到匹配的商品")
        return
    table = [[p.product_id, p.name, p.listed_price, p.stock_quantity, ", ".join(p.get_tags())] 
             for p in products]
    print(tabulate(table, headers=["ID", "商品名称", "价格", "库存", "Tags"], tablefmt="grid"))


# ==================== Product Purchase ====================
def purchase_product():
    customers = CustomerRepository().get_all()
    if not customers:
        print("请先添加客户（当前无客户）")
        return
    print(tabulate([[c.customer_id, c.contact_number, c.shipping_address]
                    for c in customers], headers=["客户ID", "电话", "地址"], tablefmt="grid"))

    customer_id = int(input("\n请选择客户 ID: "))

    all_products = []
    for v in VendorRepository().get_all():
        all_products.extend(ProductRepository().get_by_vendor(v.vendor_id))

    print(tabulate([[p.product_id, p.name, p.listed_price, p.stock_quantity]
                    for p in all_products], headers=["ID", "名称", "价格", "库存"], tablefmt="grid"))

    product_id = int(input("请选择要购买的商品 ID: "))
    quantity = int(input("购买数量: "))

    try:
        order_id, total_price, new_stock = ProductService().purchase_product(
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
        )
    except ValueError as e:
        print(f"❌ {e}")
        return

    print(f"✅ 购买成功！订单 ID = {order_id}")
    print(f"订单总价: {total_price}")
    print(f"剩余库存: {new_stock}")



    


# ==================== Order Modification ====================
def show_customer_orders():
    customer_id = int(input("\n请输入客户 ID: "))
    orders = OrderRepository().get_by_customer(customer_id)
    if not orders:
        print("该客户暂无订单")
        return
    table = [[o.order_id, o.order_date.strftime("%Y-%m-%d %H:%M"), o.total_price, o.status.value] 
             for o in orders]
    print(tabulate(table, headers=["订单ID", "日期", "总价", "状态"], tablefmt="grid"))


def modify_order():
    show_customer_orders()
    order_id = int(input("\n请输入要修改的订单 ID: "))
    
    print("\n1. 移除订单中某件商品")
    print("2. 取消整个订单（仅 PENDING 状态）")
    choice = input("请选择 (1/2): ")
    
    if choice == '1':
        # 显示订单明细（简化：实际可加 get_order_items 方法）
        print("（此处可扩展显示订单明细）")
        item_id = int(input("请输入要移除的订单明细 ID (order_item_id): "))
        OrderRepository().remove_order_item(item_id)
        print("✅ 商品已移除")
    elif choice == '2':
        OrderRepository().cancel_order(order_id)
        print("✅ 订单已取消")
    else:
        print("操作取消")