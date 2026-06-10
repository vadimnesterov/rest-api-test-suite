import pytest
import allure

from data import EXPECTED_STATUS, ServerResponse
from helpers.user_helper import UserHelper


@allure.epic("API: Users")
@allure.feature("User Login")
class TestUserLogin:

    @allure.title("Successfully log in with valid credentials")
    @allure.description("Verify that a registered user can log in with correct email and password.")
    def test_user_can_login_successfully(self, new_user_data, created_user):
        with allure.step("Send login request with valid credentials"):
            response = UserHelper.login(new_user_data)

        with allure.step("Verify response status code is 200 OK"):
            assert response.status_code == EXPECTED_STATUS.OK

        with allure.step("Verify accessToken is present in response"):
            body = response.json()
            token = body.get("accessToken")
            assert token is not None

    @allure.title("Cannot log in with a wrong password")
    @allure.description("Verify that an incorrect password returns 401 Unauthorized.")
    def test_user_cannot_login_with_wrong_password(self, new_user_data, created_user):
        with allure.step("Build login payload with an incorrect password"):
            wrong_data = dict(new_user_data)
            wrong_data["password"] = new_user_data["password"] + "X"

        with allure.step("Send login request with wrong password"):
            response = UserHelper.login(wrong_data)

        with allure.step("Verify response status code is 401 Unauthorized"):
            assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

        with allure.step("Verify error message matches WRONG_CREDENTIALS"):
            body = response.json()
            assert body.get("message") == ServerResponse.WRONG_CREDENTIALS

    @allure.title("Cannot log in with a non-existent user account")
    @allure.description("Verify that attempting to log in with unknown credentials returns 401 Unauthorized.")
    def test_user_cannot_login_nonexistent_user(self):
        with allure.step("Build login payload for a non-existent user"):
            fake_user = {
                "email": "nonexistent_user_123@example.com",
                "password": "wrongPass12345"
            }

        with allure.step("Send login request for a non-existent user"):
            response = UserHelper.login(fake_user)

        with allure.step("Verify response status code is 401 Unauthorized"):
            assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

    @allure.title("Cannot log in without a required field")
    @allure.description("Verify that login fails when email or password is omitted.")
    @pytest.mark.parametrize("missing_field", ["email", "password"])
    def test_user_cannot_login_without_required_field(self, new_user_data, missing_field):
        with allure.step(f"Remove required field '{missing_field}' from login data"):
            invalid_data = new_user_data.copy()
            invalid_data.pop(missing_field, None)

        with allure.step("Send login request with incomplete data"):
            response = UserHelper.login(invalid_data)

        with allure.step("Verify response status code is 401 Unauthorized"):
            assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

        with allure.step("Verify error message is present in response"):
            body = response.json()
            assert body.get("message") is not None
