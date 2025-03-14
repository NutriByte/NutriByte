import sys
import os

# Ensure the root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from app import scrape_links  # Now it should correctly import the function
from flask import Flask
import unittest

class TestScraper(unittest.TestCase):
    
    def setUp(self):
        """Set up a Flask test client."""
        self.app = Flask(__name__)
        self.client = self.app.test_client()

    def test_scrape_links_valid(self):
        """Test that the scraper returns a list of links for a valid webpage."""
        with self.app.test_request_context():
            response = scrape_links()
            self.assertIsInstance(response.json, list)
            self.assertTrue(len(response.json) > 0)  # At least one link expected

    def test_scrape_links_invalid(self):
        """Test handling of an invalid URL."""
        with self.app.test_request_context(query_string={"url": "https://nonexistent.url"}):
            response = scrape_links()
            self.assertIsInstance(response.json, list)  # Should return an empty list or error

if __name__ == "__main__":
    unittest.main()
