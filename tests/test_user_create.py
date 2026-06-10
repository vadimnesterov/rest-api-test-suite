import pytest
import allure

from data import EXPECTED_STATUS
from helpers.user_helper import UserHelper


@allure.epic("API: Users")
@allure.feature("User Registration")
class TestUserCreate:

    @allure.title("Successfully create a new unique user")
    @allure.description("Verify that a new user with unique credentials can be registered successfully.")
    def test_user_can_be_created_successfully(self, new_user_data):
        with allure.step("Send registration request for a new user"):
            response = UserHelper.register(new_user_data)

        with allure.step("Verify response status code is 200 OK"):
            assert response.status_code == EXPECTED_STATUS.OK

        with allure.step("Verify success=True and accessToken is present in response"):
            body = response.json()

            assert "success" in body, "Field 'success' is missing from response"
            assert body["success"] is True, "Expected success=True"

            assert "accessToken" in body, "Field 'accessToken' is missing from response"
            assert body["accessToken"] is not None, "accessToken is missing or None"

    @allure.title("Cannot create a user that is already registered")
    @allure.description("Verify that re-registering with the same credentials returns an error.")
    def test_cannot_create_user_that_already_exists(self, new_user_data, created_user):
        with allure.step("Send a duplicate registration request"):
            response = UserHelper.register(new_user_data)

        with allure.step("Verify response status code is 403 Forbidden"):
            assert response.status_code == EXPECTED_STATUS.FORBIDDEN

        with allure.step("Verify success=False and error message is present"):
            body = response.json()

            assert "success" in body, "Field 'success' is missing from response"
            assert body["success"] is False, "Expected success=False"

            assert "message" in body, "Field 'message' is missing from response"
            assert body["message"] is not None, "Error message is missing"

    @allure.title("Cannot create a user without a required field")
    @allure.description("Verify that registration fails when email, password, or name is omitted.")
    @pytest.mark.parametrize("field_to_remove", ["email", "password", "name"])
    def test_cannot_create_user_without_required_field(self, new_user_data, field_to_remove):
        with allure.step(f"Remove required field '{field_to_remove}' from user data"):
            invalid_data = new_user_data.copy()
            invalid_data.pop(field_to_remove, None)

        with allure.step("Send registration request with incomplete data"):
            response = UserHelper.register(invalid_data)

        with allure.step("Verify response status code is 403 Forbidden"):
            assert response.status_code == EXPECTED_STATUS.FORBIDDEN

        with allure.step("Verify success=False and error message is present"):
            body = response.json()

            assert "success" in body, "Field 'success' is missing from response"
            assert body["success"] is False, "Expected success=False"

            assert "message" in body, "Field 'message' is missing from response"
            assert body["message"] is not None, "Error message is missing"
