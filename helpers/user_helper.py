import requests
from faker import Faker

from data import Urls

fake = Faker()


class UserHelper:
    """
    Класс-хелпер для работы с пользователями:
    генерация данных, регистрация, логин, удаление.
    """

    @staticmethod
    def generate_user():
        """
        Создаёт словарь с данными нового пользователя.
        Никаких API-вызовов — только генерация данных.
        """
        return {
            "email": fake.email(),
            "password": fake.password(length=10),
            "name": fake.first_name(),
        }

    @staticmethod
    def register(user_data: dict):
        """
        POST /auth/register
        Регистрация нового пользователя.
        """
        return requests.post(
            f"{Urls.BASE_URL}{Urls.REGISTER}",
            json=user_data,
        )

    @staticmethod
    def login(user_data: dict):
        """
        POST /auth/login
        Логин существующего пользователя.
        """
        return requests.post(
            f"{Urls.BASE_URL}{Urls.LOGIN}",
            json=user_data,
        )

    @staticmethod
    def delete_user(token: str):
        """
        DELETE /auth/user
        Удаление пользователя по токену.
        """
        if token and not token.startswith("Bearer "):
            token = f"Bearer {token}"

        headers = {"Authorization": token}

        return requests.delete(
            f"{Urls.BASE_URL}{Urls.USER}",
            headers=headers,
        )
