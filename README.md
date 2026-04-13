# COMP7640 E-COMMERCE PLATFORM

## Modules
### Product Purchase

The Product Purchase module supports purchase processing in the system.
It validates the input, checks product availability, creates the corresponding order and transaction records, and stores which customer purchased which product in the database.

### Database Tables Involved

The Product Purchase module interacts with multiple database tables to complete a purchase process:

`orders`: stores the basic information of each order, including customer ID and total price.
`order_items`: records the details of each purchased product, including product ID, quantity, and price at the time of purchase.
`transactions`: stores the payment information for each order, including the total amount and the vendor involved.
`products`: updates the stock quantity after a successful purchase.

### Purchase Workflow

The purchase process follows these steps:

1. The system displays all available customers and products.
2. The user selects a customer, a product, and inputs the purchase quantity.
3. The system validates the input, including checking whether the quantity is valid and whether the product exists.
4. The system checks if there is sufficient stock for the selected product.
5. A new order is created and stored in the `orders` table.
6. The purchased product details are recorded in the `order_items` table.
7. A transaction record is created in the `transactions` table.
8. The stock quantity of the product is updated in the `products` table.