class OrderService:
  def __init__(self, order_repo, product_repo):
    self.order_repo = order_repo
    self.product_repo = product_repo

  def place_order(self, customer_id, cart_items):
    """
    cart_items: list of {'product_id': id, 'quantity': q, 'vendor_id': v, 'price': p}
    """

    vendor_amounts = {}
    order_items_data = []

    for item in cart_items:
      p_id = item['product_id']
      v_id = item['vendor_id']
      qty = item['quantity']
      price = item['price']

      vendor_amounts[v_id] = vendor_amounts.get(v_id, 0) + (price * qty)
      order_items_data.append((p_id, qty, price))
    try:
      order_id = self.order_repo.create_order_with_transaction(
        customer_id, 
        order_items_data, 
        vendor_amounts
      )
      return {"success": True, "order_id": order_id}
    except Exception as e:
      return {"success": False, "error": str(e)}

  def cancel_order(self, order_id):
    order = self.order_repo.get_order_details(order_id)
    if not order:
      return "Order not found"

    if order['status'] in ['SHIPPED', 'DELIVERED']:
      return "Cannot cancel: Order has already been shipped or delivered."
    
    self.order_repo.update_status(order_id, 'CANCELLED')
    return "Order cancelled successfully."
  
  def remove_product_from_order(self, order_id, order_item_id):
        order = self.order_repo.get_order_details(order_id)
        if not order or order['status'] != 'PENDING':
            return "Cannot modify: Order is already processing or shipped."

        items = self.order_repo.get_order_items(order_id)
        target_item = next((i for i in items if i['order_item_id'] == order_item_id), None)
        if not target_item:
            return "Item not found in this order."

        new_total = float(order['total_price']) - (float(target_item['price_at_purchase']) * target_item['quantity'])
        
        if new_total <= 0:
            return self.cancel_order(order_id)
        
        self.order_repo.remove_item_by_id(order_item_id, order_id, new_total)
        return "Product removed and total price updated."