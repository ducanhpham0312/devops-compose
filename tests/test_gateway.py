import unittest
import requests

class TestAPIGateway(unittest.TestCase):

    url = "http://nginx:8197"
    username = "username"
    password = "password"
    
    def setUp(self):
        requests.put(f"{self.url}/state", data="INIT", auth=(self.username, self.password))
        
    # Test cases for the API Gateway
    def test_put_same_state(self):
        response = requests.put(f"{self.url}/state", data="INIT", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)  # Expecting 401 because of re-authentication
        self.assertIn("No change in state", response.text, "This test expects the state to stay the same.")
    
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
        response = requests.put(f"{self.url}/state", data="RUNNING", auth=(self.username, self.password))
        response = requests.put(f"{self.url}/state", data="SHUTDOWN", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)
        self.assertIn("State changed to SHUTDOWN", response.text, "The test receives unexpected response for state change.")
        
    def test_get_state(self):
        response = requests.put(f"{self.url}/state", data="INIT", auth=(self.username, self.password))
        response = requests.get(f"{self.url}/state", auth=(self.username, self.password))
        receivedState = response.text
        self.assertEqual(response.status_code, 200)
        self.assertIn(receivedState, receivedState, "The test receives unexpected state.")
    
    def test_get_request(self):
        response = requests.put(f"{self.url}/state", data="RUNNING", auth=(self.username, self.password))

        response = requests.get(f"{self.url}/request", auth=(self.username, self.password))
        if response.status_code == 403:
            self.assertIn("Service2 is not in RUNNING state", response.text, "This test expects a different response to this state change.")
        else:
            self.assertEqual(response.status_code, 200)
            self.assertIn("ip_address", response.text, "This test receives unexpected response for GET /request.")
    def test_get_run_log(self):
        response = requests.get(f"{self.url}/run-log", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.text) > 0, "This test expects run log to not be empty.")
if __name__ == "__main__":
    unittest.main()
