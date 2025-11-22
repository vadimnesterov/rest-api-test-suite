import requests
from data import Urls
from faker import Faker


fake = Faker()


class UserHelper:
# создание, регистрация, логин, удаление.

    @staticmethod
    def generate_user():
        """
        Минимальная генерация данных пользователя.
        Тут только значения — никаких API-вызовов.
        """
        return {
            "email": fake.email(),
            "password": fake.password(length=10),
            "name": fake.first_name()
        }


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
