import requests
from faker import Faker

from data import Urls

fake = Faker()


class UserHelper:
    """Helpers for user management: data generation, registration, login, deletion."""

    @staticmethod
    def generate_user():
        """Return a dict with randomly generated user credentials."""
        return {
            "email": fake.email(),
            "password": fake.password(
                length=10,
                special_chars=False,
                digits=True,
                upper_case=True,
                lower_case=True,
            ),
            "name": fake.first_name(),
        }

    @staticmethod
    def register(user_data: dict):
        """POST /api/auth/register — register a new user."""
        return requests.post(
            f"{Urls.BASE_URL}{Urls.REGISTER}",
            json=user_data,
        )

    @staticmethod
    def login(user_data: dict):
        """POST /api/auth/login — log in an existing user."""
        return requests.post(
            f"{Urls.BASE_URL}{Urls.LOGIN}",
            json=user_data,
        )

    @staticmethod
    def delete_user(token: str):
        """DELETE /api/auth/user — delete the authenticated user."""
        if token and not token.startswith("Bearer "):
            token = f"Bearer {token}"

        headers = {"Authorization": token}

        return requests.delete(
            f"{Urls.BASE_URL}{Urls.USER}",
            headers=headers,
        )
