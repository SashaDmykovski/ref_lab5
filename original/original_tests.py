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
    order.add_product(product, 6)  # should not add
    assert len(order.products) == 0

def test_total_calculation(original_data):
    product, customer = original_data
    order = Order(customer)
    order.add_product(product, 2)
    assert order.calculate_total() == 40.0