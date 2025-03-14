import unittest
from unittest.mock import patch, MagicMock
import io
import sys
import food_search  

class FoodSearchTestCase(unittest.TestCase):
    def test_search_food_success(self):
        # Fake API response with one sample product
        fake_response = {
            "products": [
                {
                    "product_name": "Fake Product",
                    "brands": "Fake Brand",
                    "nutriments": {
                        "energy-kcal_100g": 100,
                        "fat_100g": 10,
                        "carbohydrates_100g": 20,
                        "proteins_100g": 5,
                        "sodium_100g": 0.1
                    }
                }
            ]
        }
        
        # Patch requests.get so we don't hit the real API
        with patch('food_search.requests.get') as mocked_get:
            mocked_response = MagicMock()
            mocked_response.status_code = 200
            mocked_response.json.return_value = fake_response
            mocked_get.return_value = mocked_response

            result = food_search.search_food("Fake Query")
            self.assertEqual(result, fake_response["products"])

    def test_search_food_failure(self):
        # Simulate an API failure (non-200 response)
        with patch('food_search.requests.get') as mocked_get:
            mocked_response = MagicMock()
            mocked_response.status_code = 404
            mocked_get.return_value = mocked_response

            result = food_search.search_food("Fake Query")
            self.assertEqual(result, [])

    def test_print_product_info_no_products(self):
        # Capture output for no products scenario
        captured_output = io.StringIO()
        sys.stdout = captured_output

        food_search.print_product_info([])
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("No products found.", output)

    def test_print_product_info_with_product(self):
        # Fake product data for testing print_product_info
        fake_products = [{
            "product_name": "Test Product",
            "brands": "Test Brand",
            "nutriments": {
                "energy-kcal_100g": 150,
                "fat_100g": 8,
                "carbohydrates_100g": 30,
                "proteins_100g": 10,
                "sodium_100g": 0.5
            }
        }]
        captured_output = io.StringIO()
        sys.stdout = captured_output

        food_search.print_product_info(fake_products)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Product #1", output)
        self.assertIn("Name: Test Product", output)
        self.assertIn("Brand(s): Test Brand", output)
        self.assertIn("Calories per 100g: 150", output)

if __name__ == '__main__':
    unittest.main()
