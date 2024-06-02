import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestShoppingCartEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.shoppingCartService.add_item_to_cart')
    def test_add_item_to_cart(self, mock_add_item_to_cart):
        customer_id = fake.random_number(digits=5)
        product_id = fake.random_number(digits=5)
        quantity = fake.random_number(digits=2)
        mock_add_item_to_cart.return_value = True

        payload = {
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": quantity
            }
        
        response = self.app.post('/shopping-cart/add-item', json=payload)

        self.assertEqual(response.status_code, 200)

    @patch('services.shoppingCartService.remove_item_from_cart')
    def test_remove_item_from_cart(self, mock_remove_item_from_cart):
        customer_id = fake.random_number(digits=5)
        product_id = fake.random_number(digits=5)
        mock_remove_item_from_cart.return_value = True

        payload = {
                "customer_id": customer_id,
                "product_id": product_id
            }

        response = self.app.delete('/shopping-cart/remove-item', json=payload)

        self.assertEqual(response.status_code, 200)

    @patch('services.shoppingCartService.update_item_quantity')
    def test_update_item_quantity(self, mock_update_item_quantity):
        customer_id = fake.random_number(digits=5)
        product_id = fake.random_number(digits=5)
        quantity = fake.random_number(digits=2)
        mock_update_item_quantity.return_value = True

        payload = {
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": quantity
            }
        
        response = self.app.put('/shopping-cart/update-quantity', json=payload)

        self.assertEqual(response.status_code, 200)

    def test_get_shopping_cart(self):
        response = self.app.get('/shopping-cart/')
        self.assertEqual(response.status_code, 200)

    def test_empty_shopping_cart(self):
        response = self.app.delete('/shopping-cart/empty')
        self.assertEqual(response.status_code, 200)
