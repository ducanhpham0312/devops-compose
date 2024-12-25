import unittest
import requests

class TestAPIGateway(unittest.TestCase):

    BASE_URL = "http://nginx:8197"
    username = "username"
    password = "password"

    # Test cases for the API Gateway
    def test_put_state_init(self):
        response = requests.put(f"{self.BASE_URL}/state", data="INIT", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)
        self.assertIn("No change in state", response.text, "This test expects no change in state.")

if __name__ == "__main__":
    unittest.main()
