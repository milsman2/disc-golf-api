"""
Locust Event Results Load Test

This file contains Locust load tests for the event results endpoints of
the Disc Golf API.

Usage:
    1. Install Locust (if not already installed):
        pip install locust
    2. Run the tests:
        locust -f locust_tests/locust_event_results.py
    3. Open your browser and go to http://localhost:8089 to start the test
    and set parameters.

Structure:
    - Simulates users making requests to the event results API endpoints.
    - Customize endpoints and user behavior by editing the tasks in this file.

Notes:
    - Adjust endpoint paths to match your API.
    - Add more tasks to simulate different user actions.
    - For more information, see: https://docs.locust.io/en/stable/
"""

from locust import HttpUser, between, task


class APITestUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_event_results(self):
        self.client.get("/api/v1/event-results/")
