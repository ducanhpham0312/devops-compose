"""Test cases for the gateway service."""

import unittest
import requests

class TestGateway(unittest.TestCase):
    """Test cases for the gateway service."""

    def setUp(self):
        """Set up the test case."""
        self.url = "http://nginx:8197"
        self.username = "username"
        self.password = "password"

    def test_get_page(self):
        """Test that the main page is accessible."""
        response = requests.get(self.url, auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)

    def test_get_info(self):
        """Test that the info endpoint is accessible."""
        response = requests.get(f"{self.url}/info", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)

    def test_stop_containers(self):
        """Test that the stop endpoint is accessible."""
        response = requests.post(f"{self.url}/stop", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)

    def test_change_state(self):
        """Test changing the state."""
        response = requests.put(
            f"{self.url}/state",
            data="RUNNING",
            auth=(self.username, self.password),
            headers={"Content-Type": "text/plain"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("State changed to RUNNING", response.text)

    def test_get_state(self):
        """Test getting the current state."""
        response = requests.get(f"{self.url}/state", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)
        received_state = response.text.strip()
        self.assertIn(received_state, ["INIT", "RUNNING", "PAUSED", "SHUTDOWN"])

    def test_get_run_log(self):
        """Test that the run log endpoint is accessible."""
        response = requests.get(f"{self.url}/run-log", auth=(self.username, self.password))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.text) > 0, "This test expects run log to not be empty.")

if __name__ == "__main__":
    unittest.main()
