import unittest
import requests

class TestAPIGateway(unittest.TestCase):

    url = "http://nginx:8197"
    username = "username"
    password = "password"

    # Test cases for the API Gateway
    def test_put_state_init(self):
        response = requests.put(f"{self.url}/state", data="INIT", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 401)  # Expecting 401 because of re-authentication
        self.assertIn("Please re-authenticate", response.text, "This test expects a re-authenticate message.")
    
    def test_put_state_running(self):
        response = requests.put(f"{self.url}/state", data="RUNNING", auth=(self.username, self.password))
        self.assertIn(response.status_code, [200, 403])
        if response.status_code == 403:
            self.assertIn("Login required", response.text, "Expected login required response")
        else:
            self.assertIn("State changed to RUNNING", response.text, "The test receives unexpected response for state change.")
    
    def test_put_state_paused_invalid(self):
        response = requests.put(f"{self.url}/state", data="PAUSED", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 403)
        self.assertIn("Cannot change state to PAUSED from", response.text, "The test receives unexpected response for invalid state change.")
    
    def test_put_state_shutdown(self):
        response = requests.put(f"{self.url}/state", data="SHUTDOWN", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)
        self.assertIn("State changed to SHUTDOWN", response.text, "The test receives unexpected response for state change.")
if __name__ == "__main__":
    unittest.main()
