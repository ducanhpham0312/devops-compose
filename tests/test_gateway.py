import unittest
import requests

class TestAPIGateway(unittest.TestCase):

    BASE_URL = "http://nginx:8197"
    username = "username"
    password = "password"

    # Test cases for the API Gateway
    def test_put_state_init(self):
        response = requests.put(f"{self.BASE_URL}/state", data="INIT", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 401)  # Expecting 401 because of re-authentication
        self.assertIn("Please re-authenticate", response.text, "Expected re-authenticate message")

if __name__ == "__main__":
    unittest.main()
