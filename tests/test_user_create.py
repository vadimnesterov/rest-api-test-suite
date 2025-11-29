# version: v1.1

import pytest
import allure

from data import EXPECTED_STATUS
from helpers.user_helper import UserHelper


@allure.epic("API: Пользователи")
@allure.feature("Создание пользователя")
class TestUserCreate:

    @allure.title("Успешное создание нового пользователя")
    @allure.description("Проверяем, что новый уникальный пользователь может быть успешно создан.")
    def test_user_can_be_created_successfully(self, new_user_data):
        with allure.step("Отправить запрос регистрации нового пользователя"):
            response = UserHelper.register(new_user_data)

        with allure.step("Проверить код ответа 200 OK"):
            assert response.status_code == EXPECTED_STATUS.OK

        with allure.step("Проверить success=True и наличие accessToken"):
            body = response.json()

            assert "success" in body, "Поле 'success' отсутствует в ответе"
            assert body["success"] is True, "Ожидалось success=True"

            assert "accessToken" in body, "Поле 'accessToken' отсутствует в ответе"
            assert body["accessToken"] is not None, "accessToken отсутствует или равен None"

    @allure.title("Нельзя создать пользователя, который уже зарегистрирован")
    @allure.description("Повторная регистрация с теми же данными должна вернуть ошибку.")
    def test_cannot_create_user_that_already_exists(self, new_user_data, created_user):
        with allure.step("Отправить повторный запрос регистрации"):
            response = UserHelper.register(new_user_data)

        with allure.step("Проверить код ответа 403 Forbidden"):
            assert response.status_code == EXPECTED_STATUS.FORBIDDEN

        with allure.step("Проверить, что success=False и есть сообщение об ошибке"):
            body = response.json()

            assert "success" in body, "Поле 'success' отсутствует в ответе"
            assert body["success"] is False, "Ожидалось success=False"

            assert "message" in body, "Поле 'message' отсутствует в ответе"
            assert body["message"] is not None, "Сообщение об ошибке отсутствует"

    @allure.title("Нельзя создать пользователя без обязательного поля")
    @allure.description("Проверяем, что регистрация невозможна без email, password или name.")
    @pytest.mark.parametrize("field_to_remove", ["email", "password", "name"])
    def test_cannot_create_user_without_required_field(self, new_user_data, field_to_remove):
        with allure.step(f"Удалить обязательное поле '{field_to_remove}' из данных пользователя"):
            invalid_data = new_user_data.copy()
            invalid_data.pop(field_to_remove, None)

        with allure.step("Отправить запрос регистрации с неполными данными"):
            response = UserHelper.register(invalid_data)

        with allure.step("Проверить код ответа 403 Forbidden"):
            assert response.status_code == EXPECTED_STATUS.FORBIDDEN

        with allure.step("Проверить, что success=False и присутствует сообщение об ошибке"):
            body = response.json()

            assert "success" in body, "Поле 'success' отсутствует в ответе"
            assert body["success"] is False, "Ожидалось success=False"

            assert "message" in body, "Поле 'message' отсутствует в ответе"
            assert body["message"] is not None, "Сообщение об ошибке отсутствует"
