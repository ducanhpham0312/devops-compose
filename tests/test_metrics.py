"""Tests for getting metrics"""

import unittest
import time
import requests

class TestMetrics(unittest.TestCase):
    """Tests for getting metrics"""
    url = "http://localhost:8197"
    def test_get_metrics(self):
        """Tests for getting metrics"""
        username = "username"
        password = "password"

        response = requests.get(f"{self.url}/metrics", auth=(username, password))
        self.assertEqual(response.status_code, 200)
        initial_metrics = response.json()
        initial_uptime = float(initial_metrics.get('Uptime').split(" ")[0])

        time.sleep(5)

        response = requests.get(f"{self.url}/metrics", auth=(username, password))
        self.assertEqual(response.status_code, 200)
        updated_metrics = response.json()
        updated_uptime = float(updated_metrics.get('Uptime').split(" ")[0])

        self.assertGreater(updated_uptime, initial_uptime, "This test expects a bigger uptime.")

if __name__ == "__main__":
    unittest.main()
