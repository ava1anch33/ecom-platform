import sys

class EcommerceCLI:
  def __init__(self, controller):
    self.controller = controller

  def start(self):
    print("=== COMP7640 E-Commerce Platform ===")
    menu = {
      "a1": ("Display a listing of all vendors", self.list_vendors_action),
      "a2": ("Onboard new vendors onto the marketplace", self.run_onboard_vendor),
      "p1": ("Browse all products offered by each vendor", self.list_products_grouped_by_vendor_action),
      "p2": ("Introduce new products to a vendor's catalog.", self.add_product_action),
      "p3": ("Product Discovery", self.run_search),
      "p4": ("Product Purchase", self.run_place_order),
      "o0": ("View Order Items Details", self.show_order_items_details),
      "o1": ("List Orders by Customer", self.list_order_by_customer),
      "o2": ("Cancel Order", self.run_cancel_order),
      "o3": ("Modify Order", self.run_modify_order),
      "0": ("Exit", sys.exit)
    }
    while True:
      print("\n" + "="*20)
      for k, v in menu.items(): print(f"{k}. {v[0]}")
      choice = input("Select: ")
      if choice in menu: menu[choice][1]()

  # Display a listing of all vendors
  def list_vendors_action(self):
    res = self.controller.list_vendors_action()
    if res["status"] == "success":
      for v in res["data"]:
        print(f"ID:{v['vendor_id']} | {v['business_name']} | {v['geographical_presence']}")
    else:
      print(f"Error: {res['message']}")

  # Onboard new vendors onto the marketplace
  def run_onboard_vendor(self):
    name = input("Vendor Name: ")
    loc = input("Location: ")
    res = self.controller.onboard_vendor_action(name, loc)
    print(f"[{res['status'].upper()}] {res.get('data', '')} {res['message']}")

  # Browse all products offered by each vendor
  def list_products_grouped_by_vendor_action(self):
    res = self.controller.list_vendors_action()
    if res["status"] == "success":
      for v in res["data"]:
        print(f"\nVendor: {v['business_name']} (ID: {v['vendor_id']})")
        prod_res = self.controller.list_vendor_products_action(v['vendor_id'])
        if prod_res["status"] == "success":
          for p in prod_res["data"]:
            print(f"  - ID:{p['product_id']} | {p['name']} | ${p['listed_price']} | Stock:{p['stock_quantity']} | Tags:{p['tag1']}, {p['tag2']}, {p['tag3']}")
        else:
          print(f"  Error fetching products: {prod_res['message']}")
    else:
      print(f"Error: {res['message']}")

  # Introduce new products to a vendor's catalog.
  def add_product_action(self):
    try:
      v_id = int(input("Vendor ID: "))
      name = input("Product Name: ")
      price = float(input("Price: "))
      stock = int(input("Stock Quantity: "))
      tags = input("Tags (comma separated, max 3): ").split(",")[:3]
      res = self.controller.add_product_action(v_id, name, price, stock, tags)
      print(f"[{res['status'].upper()}] {res['message']}")
    except ValueError:
      print("Invalid input format.")

  # Product Discovery
  def run_search(self):
    kw = input("Search Tag/Name: ")
    res = self.controller.search_products_action(kw)
    if res["status"] == "success":
      for p in res["data"]:
        print(f"ID:{p['product_id']} | {p['name']} | ${p['listed_price']} | Stock:{p['stock_quantity']} | Tags:{p['tag1']}, {p['tag2']}, {p['tag3']}")
    else:
      print(f"Error: {res['message']}")

  # Product Purchasing
  def run_place_order(self):
    try:
      c_id = int(input("Customer ID: "))
      cart = []
      while True:
        p_id = input("Product ID (or 'd' for done): ")
        if p_id == 'd': break
        qty = int(input("Quantity: "))
        v_id = int(input("Vendor ID: "))
        price = float(input("Price: "))
        cart.append({'product_id': int(p_id), 'quantity': qty, 'vendor_id': v_id, 'price': price})
      
      res = self.controller.place_order_action(c_id, cart)
      print(f"{res['message']} ID: {res.get('data', '')}")
    except ValueError:
      print("Invalid input format.")

  def list_order_by_customer(self):
    c_id = input("Customer ID: ")
    res = self.controller.get_order_history_action(int(c_id))
    if res["status"] == "success":
      for o in res["data"]:
        print(f"Order ID:{o['order_id']} | Total:${o['total_price']} | Status:{o['status']} | Placed At:{o['order_date']}")
    else:
      print(f"Error: {res['message']}")

  def show_order_items_details(self):
    o_id = input("Order ID: ")
    res = self.controller.get_order_items_details_action(int(o_id))
    if res["status"] == "success":
      for item in res["data"]:
        print(f"Product ID:{item['product_id']} | Quantity:{item['quantity']} | Price at Purchase:${item['price_at_purchase']}")
    else:
      print(f"Error: {res['message']}")

  def run_cancel_order(self):
    o_id = input("Order ID to cancel: ")
    res = self.controller.cancel_order_action(int(o_id))
    print(res["message"])

  def run_modify_order(self):
    print("\n1. Remove specific product from order")
    print("2. Cancel entire order")
    sub_choice = input("Select: ")
    
    o_id = int(input("Order ID: "))
    if sub_choice == '1':
        # get order item name and id to show to user
        product_name = self.controller.get_order_items_details_action(o_id)
        print("Products in this order:")
        for item in product_name["data"]:
            print(f"Order Item ID:{item['order_item_id']} | Product ID:{item['product_id']} | Quantity:{item['quantity']} | Price at Purchase:${item['price_at_purchase']}")

        item_id = int(input("Order Item ID to remove: "))
        res = self.controller.remove_order_item_action(o_id, item_id)
        print(res["message"])
    elif sub_choice == '2':
        res = self.controller.cancel_order_action(o_id)
        print(res["message"])

