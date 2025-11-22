import pytest
import allure

from data import EXPECTED_STATUS, ServerResponse
from helpers.user_helper import UserHelper


@allure.epic("API: Пользователи")
@allure.feature("Авторизация")
class TestUserLogin:

    @allure.title("Успешный вход зарегистрированного пользователя")
    @allure.description("Проверяем, что пользователь с корректными логином и паролем может войти в систему.")
    def test_user_can_login_successfully(self, new_user_data, created_user):
        with allure.step("Отправить запрос логина с валидными данными"):
            response = UserHelper.login(new_user_data)

        with allure.step("Проверить статус-код 200 OK"):
            assert response.status_code == EXPECTED_STATUS.OK

        with allure.step("Проверить наличие accessToken в ответе"):
            body = response.json()
            token = body.get("accessToken")
            assert token is not None

    @allure.title("Нельзя авторизоваться с неверным паролем")
    @allure.description("Проверяем, что при неправильном пароле сервер возвращает 401 Unauthorized.")
    def test_user_cannot_login_with_wrong_password(self, new_user_data, created_user):
        with allure.step("Сформировать данные логина с неверным паролем"):
            wrong_data = dict(new_user_data)
            wrong_data["password"] = new_user_data["password"] + "X"

        with allure.step("Отправить запрос логина с неверным паролем"):
            response = UserHelper.login(wrong_data)

        with allure.step("Проверить статус-код 401 Unauthorized"):
            assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

        with allure.step("Проверить сообщение об ошибке WRONG_CREDENTIALS"):
            body = response.json()
            assert body.get("message") == ServerResponse.WRONG_CREDENTIALS

    @allure.title("Нельзя авторизоваться несуществующим пользователем")
    @allure.description("Проверяем, что попытка входа с несуществующей учетной записью приводит к ошибке.")
    def test_user_cannot_login_nonexistent_user(self):
        with allure.step("Сформировать данные для несуществующего пользователя"):
            fake_user = {
                "email": "nonexistent_user_123@example.com",
                "password": "wrongPass12345"
            }

        with allure.step("Отправить запрос логина несуществующего пользователя"):
            response = UserHelper.login(fake_user)

        with allure.step("Проверить статус-код 401 Unauthorized"):
            assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

    @allure.title("Нельзя авторизоваться без обязательного поля")
    @allure.description("Проверяем, что логин невозможен без email или password.")
    @pytest.mark.parametrize("missing_field", ["email", "password"])
    def test_user_cannot_login_without_required_field(self, new_user_data, missing_field):
        with allure.step(f"Удалить обязательное поле '{missing_field}' из данных логина"):
            invalid_data = new_user_data.copy()
            invalid_data.pop(missing_field, None)

        with allure.step("Отправить запрос логина с неполными данными"):
            response = UserHelper.login(invalid_data)

        with allure.step("Проверить статус-код 401 Unauthorized"):
            assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

        with allure.step("Проверить, что сервер вернул сообщение об ошибке"):
            body = response.json()
            assert body.get("message") is not None
