import json
import random
from typing import Dict, Optional
from locust import HttpUser, task, between
from locust.clients import HttpSession

class AuthUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    host = "http://localhost:8888"  # Your API host
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token: Optional[str] = None
        self.user_data: Dict = {
            "email": f"test_user_{random.randint(1, 1000000)}@example.com",
            "password": "TestPassword123!",
            "full_name": f"Test User {random.randint(1, 1000000)}"
        }

    def on_start(self):
        """Initialize user data before starting tasks."""
        # Register a new user
        try:
            response = self.client.post(
                "/api/v1/auth/register",
                json=self.user_data
            )
            if response.status_code == 200:
                self.logger.info(f"Successfully registered user: {self.user_data['email']}")
            else:
                self.logger.error(f"Failed to register user: {response.text}")
        except Exception as e:
            self.logger.error(f"Error during registration: {str(e)}")

    @task(3)
    def login(self):
        """Test login endpoint."""
        try:
            response = self.client.post(
                "/api/v1/auth/login",
                json={
                    "email": self.user_data["email"],
                    "password": self.user_data["password"]
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.logger.info("Successfully logged in")
            else:
                self.logger.error(f"Login failed: {response.text}")
        except Exception as e:
            self.logger.error(f"Error during login: {str(e)}")

    @task(2)
    def get_profile(self):
        """Test getting user profile."""
        if not self.token:
            self.login()
            if not self.token:
                return

        try:
            response = self.client.get(
                "/api/v1/users/me",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                self.logger.info("Successfully retrieved profile")
            else:
                self.logger.error(f"Failed to get profile: {response.text}")
        except Exception as e:
            self.logger.error(f"Error getting profile: {str(e)}")

    @task(1)
    def refresh_token(self):
        """Test token refresh."""
        if not self.token:
            self.login()
            if not self.token:
                return

        try:
            response = self.client.post(
                "/api/v1/auth/refresh",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.logger.info("Successfully refreshed token")
            else:
                self.logger.error(f"Token refresh failed: {response.text}")
        except Exception as e:
            self.logger.error(f"Error refreshing token: {str(e)}")

    @task(1)
    def logout(self):
        """Test logout endpoint."""
        if not self.token:
            return

        try:
            response = self.client.post(
                "/api/v1/auth/logout",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                self.token = None
                self.logger.info("Successfully logged out")
            else:
                self.logger.error(f"Logout failed: {response.text}")
        except Exception as e:
            self.logger.error(f"Error during logout: {str(e)}") 