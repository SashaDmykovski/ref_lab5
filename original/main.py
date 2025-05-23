import json
import smtplib
from datetime import datetime

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
        self.created_at = datetime.now()
        self.status = 'pending'

    def add_product(self, product, quantity):
        if product.is_available(quantity):
            self.products.append((product, quantity))
            product.reduce_stock(quantity)
        else:
            print(f"Not enough stock for {product.name}")

    def calculate_total(self):
        return sum([product.price * quantity for product, quantity in self.products])

    def generate_invoice(self):
        invoice = f"Invoice for {self.customer.name}\nDate: {self.created_at.strftime('%Y-%m-%d')}\n"
        for product, quantity in self.products:
            invoice += f"{product.name}: {quantity} x {product.price} = {product.price * quantity}\n"
        invoice += f"Total: {self.calculate_total()}\n"
        return invoice

    def save_invoice_to_file(self):
        invoice = self.generate_invoice()
        with open(f"invoice_{self.customer.customer_id}.txt", "w") as f:
            f.write(invoice)

    def send_email_confirmation(self):
        message = self.generate_invoice()
        server = smtplib.SMTP('smtp.mailtrap.io')
        server.login('user', 'pass')
        server.sendmail("shop@example.com", self.customer.email, message)
        server.quit()

    def confirm_payment(self, method):
        if method == "credit_card":
            print("Processing credit card payment...")
        elif method == "paypal":
            print("Redirecting to PayPal...")
        else:
            print("Unknown payment method")
        self.status = 'paid'

    def arrange_delivery(self, delivery_type):
        if delivery_type == "standard":
            print(f"Delivering to {self.customer.address} in 3-5 days.")
        elif delivery_type == "express":
            print(f"Express delivery to {self.customer.address} in 1 day.")
        else:
            print("Invalid delivery option")

class OrderManager:
    def __init__(self):
        self.orders = []

    def create_order(self, customer):
        order = Order(customer)
        self.orders.append(order)
        return order

    def export_orders_to_json(self):
        export_data = []
        for order in self.orders:
            export_data.append({
                "customer": order.customer.name,
                "email": order.customer.email,
                "total": order.calculate_total(),
                "status": order.status
            })
        with open("orders_export.json", "w") as f:
            json.dump(export_data, f, indent=4)
