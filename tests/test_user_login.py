import pytest
import allure

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

def test_user_cannot_login_nonexistent_user():
    """
    Негативный сценарий:
    попытка логина несуществующего пользователя должна завершиться ошибкой.
    """
    # Формируем данные пользователя, которого нет в системе
    fake_user = {
        "email": "nonexistent_user_123@example.com",
        "password": "wrongPass12345"
    }

    # Пытаемся выполнить логин несуществующего пользователя
    response = UserHelper.login(fake_user)

    # Проверяем статус-код (401 Unauthorized — нет таких учётных данных)
    assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED


@pytest.mark.parametrize("missing_field", ["email", "password"])
def test_user_cannot_login_without_required_field(new_user_data, missing_field):
    """
    Негативный сценарий:
    логин невозможен, если отсутствует одно из обязательных полей.
    """
    # Удаляем обязательное поле, указанное в параметре (email или password)
    invalid_data = new_user_data.copy()
    invalid_data.pop(missing_field, None)

    # Делаем запрос логина с неполными данными
    response = UserHelper.login(invalid_data)

    # Проверяем статус-код (401 Unauthorized — учетные данные некорректные или неполные)
    assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

    # Получаем тело ответа
    body = response.json()

    # Проверяем, что сервер вернул поле message — признак корректной обработки ошибки
    assert body.get("message") is not None