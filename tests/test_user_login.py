import pytest

from data import EXPECTED_STATUS, ServerResponse
from helpers.user_helper import UserHelper


def test_user_can_login_successfully(new_user_data, created_user):
    """
    Позитивный сценарий:
    зарегистрированный пользователь может зайти в систему.
    """
    # Делаем запрос логина теми же данными, что использовали при регистрации
    response = UserHelper.login(new_user_data)

    # Проверяем статус-код (200 OK — успешная авторизация)
    assert response.status_code == EXPECTED_STATUS.OK

    # Получаем тело ответа
    body = response.json()

    # Проверяем, что сервер вернул accessToken — признак успешного логина
    token = body.get("accessToken")
    assert token is not None


def test_user_cannot_login_with_wrong_password(new_user_data, created_user):
    """
    Негативный сценарий:
    логин с неверным паролем должен быть отклонён.
    """
    # Берём те же данные пользователя, но изменяем пароль
    wrong_data = dict(new_user_data)
    wrong_data["password"] = new_user_data["password"] + "X"

    # Делаем запрос логина с неверным паролем
    response = UserHelper.login(wrong_data)

    # Проверяем статус-код (401 Unauthorized)
    assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

    # Получаем тело ответа
    body = response.json()

    # Проверяем сообщение об ошибке
    assert body.get("message") == ServerResponse.WRONG_CREDENTIALS
