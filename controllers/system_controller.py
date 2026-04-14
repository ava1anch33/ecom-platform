class SystemController:
  def __init__(self, admin_service, product_service, order_service):
    self.admin_svc = admin_service
    self.product_svc = product_service
    self.order_svc = order_service

  # --- vendor ---
  def list_vendors_action(self):
    vendors = self.admin_svc.vendor_repo.list_all_vendors()
    return {"status": "success", "data": vendors}

  def list_vendor_products_action(self, vendor_id):
        products = self.product_svc.product_repo.get_by_vendor(vendor_id)
        return {"status": "success", "data": products}
  
  def onboard_vendor_action(self, name, location):
    if not name or not location:
      return {"status": "error", "message": "Business name and location are required."}
    v_id = self.admin_svc.onboard_vendor(name, location)
    return {"status": "success", "data": v_id, "message": "Vendor onboarded successfully."}


  # --- product ---
  def search_products_action(self, keyword):
    if not keyword:
      return {"status": "error", "message": "Search keyword cannot be empty."}
    products = self.product_svc.search_catalog(keyword)
    return {"status": "success", "data": products}

  def add_product_action(self, vendor_id, name, price, stock, tags):
    try:
      self.product_svc.add_product_to_inventory(vendor_id, name, float(price), int(stock), tags)
      return {"status": "success", "message": "Product added successfully."}
    except Exception as e:
      return {"status": "error", "message": str(e)}

  # --- order ---
  def place_order_action(self, customer_id, cart):
    if not cart:
      return {"status": "error", "message": "Cart is empty."}
    result = self.order_svc.place_order(customer_id, cart)
    if result['success']:
      return {"status": "success", "data": result['order_id'], "message": "Order placed!"}
    return {"status": "error", "message": result['error']}

  def cancel_order_action(self, order_id):
    msg = self.order_svc.cancel_order(order_id)
    if "successfully" in msg:
      return {"status": "success", "message": msg}
    return {"status": "error", "message": msg}
  
  def remove_order_item_action(self, order_id, order_item_id):
    try:
        msg = self.order_svc.remove_product_from_order(order_id, order_item_id)
        if "successfully" in msg or "updated" in msg:
            return {"status": "success", "message": msg}
        return {"status": "error", "message": msg}
    except Exception as e:
        return {"status": "error", "message": str(e)}

  def get_order_history_action(self, customer_id):
    history = self.admin_svc.customer_repo.get_order_history(customer_id)
    return {"status": "success", "data": history}
  
  def get_order_items_details_action(self, order_id):
    items = self.order_svc.order_repo.get_order_items(order_id)
    return {"status": "success", "data": items}