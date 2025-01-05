"""Test cases for nginx exercise. Should not affect the implementation of the project."""
import unittest
import requests
import os

SERVICE_HOST = os.getenv("SERVICE_HOST", "localhost")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8197")
class TestApp(unittest.TestCase):
    """Test cases for the app"""

    def test_get_page(self):
        """Test that the main page is accessible"""
        url = f"http://{SERVICE_HOST}:{SERVICE_PORT}"
        response = requests.get(url, auth=("username", "password"), timeout=10)
        self.assertEqual(response.status_code, 200)

    def test_get_info(self):
        """Test that the info endpoint is accessible"""
        url = f"http://{SERVICE_HOST}:{SERVICE_PORT}/info"
        response = requests.get(url, auth=("username", "password"), timeout=10)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
