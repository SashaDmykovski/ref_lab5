class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def is_available(self, quantity):
        return self.stock >= quantity

    def reduce_stock(self, quantity):
        self.stock -= quantity


class Customer:
    def __init__(self, customer_id, name, email, address):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.address = address


class Order:
    def __init__(self, customer):
        self.customer = customer
        self.products = []
        self.created_at = "today"
        self.status = 'pending'

    def add_product(self, product, quantity):
        if product.is_available(quantity):
            product.reduce_stock(quantity)
            self.products.append((product, quantity))
        else:
            print(f"Not enough stock for {product.name}")

    def calculate_total(self):
        return sum(product.price * quantity for product, quantity in self.products)