class ProductService:
  def __init__(self, product_repo):
    self.product_repo = product_repo

  def search_catalog(self, keyword):
    results = self.product_repo.search_by_tag(keyword)
    return [p for p in results if p['stock_quantity'] > 0]

  def add_product_to_inventory(self, vendor_id, name, price, stock, tags):
    if not tags:
      tags = []
    valid_tags = tags[:3]
    return self.product_repo.add_product(vendor_id, name, price, stock, valid_tags)