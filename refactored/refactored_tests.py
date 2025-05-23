import pytest
from refactored_code import (
    Product, Customer, Order, OrderProcessor,
    CreditCardPayment, ExpressDelivery,
    InvoiceGenerator, InvoiceSaver
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

def test_total_amount(refactored_data):
    product, customer = refactored_data
    order = Order(customer)
    order.add_item(product, 2)
    assert order.total_amount() == 100.0

def test_invoice_generation(refactored_data):
    product, customer = refactored_data
    order = Order(customer)
    order.add_item(product, 2)
    generator = InvoiceGenerator()
    invoice = generator.generate(order)
    assert "Keyboard" in invoice
    assert "Total: 100.0" in invoice

def test_order_processing(refactored_data):
    product, customer = refactored_data
    order = Order(customer)
    order.add_item(product, 2)
    processor = OrderProcessor(CreditCardPayment(), ExpressDelivery())
    processor.process_order(order)
    assert order.status == "paid"