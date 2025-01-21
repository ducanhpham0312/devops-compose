"""Test cases for the gateway service."""

import unittest
import requests
import os

class TestGateway(unittest.TestCase):
    """Test cases for the gateway service."""

    url = "http://nginx:8197"
    username = "username"
    password = "password"

    def setUp(self):
        """Set up the test case."""
        requests.put(
            f"{self.url}/state",
            data="INIT",
            auth=(self.username, self.password),
            timeout=10
        )

    def test_get_page(self):
        """Test that the main page is accessible."""
        response = requests.get(self.url, auth=(self.username, self.password), timeout=10)
        self.assertEqual(response.status_code, 200)

    def test_change_state(self):
        """Test changing the state."""
        response = requests.put(
            f"{self.url}/state",
            data="RUNNING",
            auth=(self.username, self.password),
            headers={"Content-Type": "text/plain"},
            timeout=10
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("State changed to RUNNING", response.text)

    def test_get_state(self):
        """Test getting the current state."""
        response = requests.get(
            f"{self.url}/state",
            auth=(self.username, self.password),
            timeout=10
        )
        self.assertEqual(response.status_code, 200)
        received_state = response.text.strip().strip("\"")
        self.assertIn(received_state, ["INIT", "RUNNING", "PAUSED", "SHUTDOWN"])

    def test_get_run_log(self):
        """Test that the run log endpoint is accessible."""
        response = requests.get(
            f"{self.url}/run-log",
            auth=(self.username, self.password),
            timeout=10
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.text) > 0, "This test expects run log to not be empty.")

if __name__ == "__main__":
    unittest.main()
