from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

# --- Domain Models ---

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


class OrderItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def total_price(self) -> float:
        return self.product.price * self.quantity


# --- Order ---

class Order:
    def __init__(self, customer: Customer):
        self.customer = customer
        self.items: List[OrderItem] = []
        self.created_at = datetime.now()
        self.status = 'pending'

    def add_item(self, product: Product, quantity: int):
        if product.is_available(quantity):
            product.reduce_stock(quantity)
            self.items.append(OrderItem(product, quantity))
        else:
            raise ValueError("Not enough stock")

    def total_amount(self) -> float:
        return sum(item.total_price() for item in self.items)


# --- Payment & Delivery Strategies ---

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Processing credit card payment of {amount}")


class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Redirecting to PayPal to pay {amount}")


class DeliveryStrategy(ABC):
    @abstractmethod
    def deliver(self, address: str) -> None:
        pass


class StandardDelivery(DeliveryStrategy):
    def deliver(self, address: str) -> None:
        print(f"Delivering to {address} in 3-5 days")


class ExpressDelivery(DeliveryStrategy):
    def deliver(self, address: str) -> None:
        print(f"Express delivery to {address} in 1 day")


# --- Services ---

class InvoiceGenerator:
    def generate(self, order: Order) -> str:
        lines = [f"Invoice for {order.customer.name} on {order.created_at.date()}"]
        for item in order.items:
            lines.append(f"{item.product.name}: {item.quantity} x {item.product.price} = {item.total_price()}")
        lines.append(f"Total: {order.total_amount()}")
        return "\n".join(lines)


class InvoiceSaver:
    def save_to_file(self, filename: str, invoice: str) -> None:
        with open(filename, 'w') as f:
            f.write(invoice)


class OrderProcessor:
    def __init__(self, payment: PaymentStrategy, delivery: DeliveryStrategy):
        self.payment = payment
        self.delivery = delivery

    def process_order(self, order: Order):
        amount = order.total_amount()
        self.payment.pay(amount)
        self.delivery.deliver(order.customer.address)
        order.status = "paid"