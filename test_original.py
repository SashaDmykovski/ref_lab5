import pytest
from original_code import Product, Customer, Order

@pytest.fixture
def original_data():
    product = Product(1, "Mouse", 20.0, 5)
    customer = Customer(1, "Bob", "bob@example.com", "456 Road")
    return product, customer

def test_add_product_success(original_data):
    product, customer = original_data
    order = Order(customer)
    order.add_product(product, 2)
    assert len(order.products) == 1
    assert product.stock == 3

def test_add_product_insufficient_stock(original_data):
    product, customer = original_data
    order = Order(customer)
    order.add_product(product, 6)  # перевищує склад
    assert len(order.products) == 0

def test_total_calculation(original_data):
    product, customer = original_data
    order = Order(customer)
    order.add_product(product, 2)
    assert order.calculate_total() == 40.0

def test_multiple_additions_total(original_data):
    product, customer = original_data
    order = Order(customer)
    order.add_product(product, 1)
    order.add_product(product, 2)
    assert order.calculate_total() == 60.0

def test_stock_reduction_after_order(original_data):
    product, customer = original_data
    order = Order(customer)
    order.add_product(product, 3)
    assert product.stock == 2

def test_default_order_status(original_data):
    product, customer = original_data
    order = Order(customer)
    assert order.status == "pending"

def test_order_customer_association(original_data):
    product, customer = original_data
    order = Order(customer)
    assert order.customer.name == "Bob"
    assert order.customer.email == "bob@example.com"

def test_zero_quantity_addition(original_data):
    product, customer = original_data
    order = Order(customer)
    order.add_product(product, 0)
    assert len(order.products) == 1
    assert order.calculate_total() == 0

def test_negative_quantity_addition(original_data):
    product, customer = original_data
    order = Order(customer)
    order.add_product(product, -2)
    assert len(order.products) == 1
    assert order.calculate_total() == -40.0

def test_stock_behavior_with_negative_quantity(original_data):
    product, customer = original_data
    order = Order(customer)
    order.add_product(product, -1)
    assert product.stock == 6  # Логічна помилка: -1 "збільшує" склад
