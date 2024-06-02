import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestProductsEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app("DevelopmentConfig")
        app.config["TESTING"] = True
        self.app = app.test_client()
        self.faker = Faker()

    def create_test_product(self):
        mock_product = MagicMock()
        mock_product.id = self.faker.random_number(digits=3)
        mock_product.name = self.faker.word()
        mock_product.price = float(self.faker.random_number(digits=2))
        mock_product.stock_quantity = self.faker.random_number(digits=2)

        mock_product.__getitem__.side_effect = lambda key: getattr(mock_product, key)
        return mock_product

    def create_product_payload(self, mock_product):
        return {
            "name": mock_product.name,
            "price": mock_product.price,
            "stock_quantity": mock_product.stock_quantity
        }

    @patch("services.productService.save")
    def test_save_product(self, mock_save):
        mock_product = self.create_test_product()
        mock_save.return_value = mock_product
        payload = self.create_product_payload(mock_product)
        headers = {"Authorization": f"Bearer {self.auth_token}"}

        response = self.app.post("/products/", json=payload, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["id"], mock_product.id)

    def test_get_products(self):
        response = self.app.get("/products/")
        self.assertEqual(response.status_code, 200)

    @patch("services.productService.get_product")
    def test_get_product(self, mock_get):
        mock_product = self.create_test_product()
        mock_get.return_value = mock_product

        response = self.app.get(f"/products/{mock_product.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], mock_product.name)

    @patch("services.productService.update")
    def test_update_product(self, mock_update):
        mock_product = self.create_test_product()
        new_name = self.faker.word()
        mock_product.name = new_name
        mock_update.return_value = mock_product
        payload = {"name": new_name}
        headers = {"Authorization": f"Bearer {self.auth_token}"}

        response = self.app.put(f"/products/{mock_product.id}", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], mock_product.name)

    @patch("services.productService.delete")
    def test_delete_product(self, mock_delete):
        mock_product = self.create_test_product()
        mock_delete.return_value = True
        headers = {"Authorization": f"Bearer {self.auth_token}"}

        response = self.app.delete(f"/products/{mock_product.id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], f"Product with ID {mock_product.id} has been deleted successfully")