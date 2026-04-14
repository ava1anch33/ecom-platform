class AdminService:
  def __init__(self, vendor_repo, customer_repo):
    self.vendor_repo = vendor_repo
    self.customer_repo = customer_repo

  def register_new_customer(self, name, phone, address):
    if not name or not phone:
      raise ValueError("Name and contact number are required.")
    return self.customer_repo.add_customer(name, phone, address)

  def onboard_vendor(self, name, location):
    return self.vendor_repo.onboard_new_vendor(name, location)

  def get_customer_dashboard(self, customer_id):
    profile = self.customer_repo.get_customer_by_id(customer_id)
    history = self.customer_repo.get_order_history(customer_id)
    return {
      "profile": profile,
      "order_history": history
    }