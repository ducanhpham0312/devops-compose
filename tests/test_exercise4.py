"""Test cases for nginx exercise. Should not affect the implementation of the project."""
import unittest
import requests

class TestApp(unittest.TestCase):
    """Test cases for the app"""

    def test_get_page(self):
        """Test that the main page is accessible"""
        url = "http://localhost:8197"
        response = requests.get(url, auth=("username", "password"), timeout=10)
        self.assertEqual(response.status_code, 200)

    def test_get_info(self):
        """Test that the info endpoint is accessible"""
        url = "http://localhost:8197/info"
        response = requests.get(url, auth=("username", "password"), timeout=10)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
