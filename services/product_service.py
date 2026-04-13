from repositories.product_repository import ProductRepository
from repositories.order_repository import OrderRepository
from repositories.transaction_repository import TransactionRepository
from models.order import Order
from models.order_item import OrderItem
from models.transaction import Transaction


class ProductService:
    """product purchase business logic"""

    def purchase_product(self, customer_id: int, product_id: int, quantity: int) -> tuple[int, float, int]:
        """Process product purchase and return order summary"""
        if quantity <= 0:
            raise ValueError("购买数量必须大于 0")

        product_repo = ProductRepository()
        product = product_repo.get_by_id(product_id)

        if not product:
            raise ValueError("商品不存在")

        if product.stock_quantity < quantity:
            raise ValueError("库存不足，无法完成购买")

        total_price = product.listed_price * quantity

        order = Order(customer_id=customer_id, total_price=total_price)
        order_id = OrderRepository().create_order(order)

        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_at_purchase=product.listed_price,
        )
        OrderRepository().add_order_item(item)

        transaction = Transaction(
            order_id=order_id,
            vendor_id=product.vendor_id,
            amount=total_price,
        )
        TransactionRepository().create(transaction)

        new_stock = product.stock_quantity - quantity
        product_repo.update_stock(product_id, new_stock)

        return order_id, total_price, new_stock