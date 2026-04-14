from config import DB_CONFIG
from repositories.vendor_repository import VendorRepository
from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository
from repositories.customer_repository import CustomerRepository
from services.admin_service import AdminService
from services.product_service import ProductService
from services.order_service import OrderService
from controllers.system_controller import SystemController
from cli import EcommerceCLI

def main():
  # 1. Init Repositories
  v_repo = VendorRepository(DB_CONFIG)
  p_repo = ProductRepository(DB_CONFIG)
  o_repo = OrderRepository(DB_CONFIG)
  c_repo = CustomerRepository(DB_CONFIG)

  # 2. Init Services
  admin_svc = AdminService(v_repo, c_repo)
  product_svc = ProductService(p_repo)
  order_svc = OrderService(o_repo, p_repo)

  sys_controller = SystemController(admin_svc, product_svc, order_svc)

  # 3. Start CLI
  app = EcommerceCLI(sys_controller)
  app.start()

if __name__ == "__main__":
  main()