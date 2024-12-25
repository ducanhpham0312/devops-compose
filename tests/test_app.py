import unittest
import requests

class TestApp(unittest.TestCase):
    def test_get_page(self):
        url = "http://nginx:8197"
        response = requests.get(url, auth=("username", "password"))
        self.assertEqual(response.status_code, 200)
    def test_get_info(self):
        url = "http://nginx:8197"
        response = requests.get(url, auth=("username", "password"))
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()