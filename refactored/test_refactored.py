import pytest
from refactored_code import (
    Product, Customer, Order, OrderProcessor,
    CreditCardPayment, PayPalPayment,
    StandardDelivery, ExpressDelivery,
    InvoiceGenerator
)

@pytest.fixture
def refactored_data():
    product = Product(1, "Keyboard", 50.0, 10)
    customer = Customer(1, "Alice", "alice@example.com", "123 Street")
    return product, customer

def test_add_item_success(refactored_data):
    product, customer = refactored_data
    order = Order(customer)
    order.add_item(product, 2)
    assert len(order.items) == 1
    assert product.stock == 8

def test_add_item_insufficient_stock(refactored_data):
    product, customer = refactored_data
    order = Order(customer)
    with pytest.raises(ValueError):
        order.add_item(product, 20)

def test_total_amount_calculation(refactored_data):
    product, customer = refactored_data
    order = Order(customer)
    order.add_item(product, 2)
    assert order.total_amount() == 100.0

def test_order_status_initial(refactored_data):
    product, customer = refactored_data
    order = Order(customer)
    assert order.status == "pending"

def test_order_customer_info(refactored_data):
    product, customer = refactored_data
    order = Order(customer)
    assert order.customer.name == "Alice"
    assert order.customer.email == "alice@example.com"

def test_invoice_contains_product_and_total(refactored_data):
    product, customer = refactored_data
    order = Order(customer)
    order.add_item(product, 1)
    invoice = InvoiceGenerator().generate(order)
    assert "Keyboard" in invoice
    assert "Total: 50.0" in invoice

def test_payment_strategy_credit_card(capsys):
    payment = CreditCardPayment()
    payment.pay(99.0)
    output = capsys.readouterr().out
    assert "credit card" in output.lower()

def test_payment_strategy_paypal(capsys):
    payment = PayPalPayment()
    payment.pay(99.0)
    output = capsys.readouterr().out
    assert "paypal" in output.lower()

def test_delivery_strategy_standard(capsys):
    delivery = StandardDelivery()
    delivery.deliver("Test Address")
    output = capsys.readouterr().out
    assert "3-5 days" in output

def test_order_processing_sets_paid_status(refactored_data):
    product, customer = refactored_data
    order = Order(customer)
    order.add_item(product, 2)
    processor = OrderProcessor(CreditCardPayment(), ExpressDelivery())
    processor.process_order(order)
    assert order.status == "paid"
