import requests
from data import Urls


class UserHelper:
# регистрация, логин, удаление.

    @staticmethod
    def register(user_data: dict):
        return requests.post(
            f"{Urls.BASE_URL}{Urls.REGISTER}",
            json=user_data
        )

    @staticmethod
    def login(user_data: dict):
        return requests.post(
            f"{Urls.BASE_URL}{Urls.LOGIN}",
            json=user_data
        )

    @staticmethod
    def delete_user(token: str):
        if token and not token.startswith("Bearer "):
            token = f"Bearer {token}"

        headers = {"Authorization": token}

        return requests.delete(
            f"{Urls.BASE_URL}{Urls.USER}",
            headers=headers
        )
