import allure

from data import EXPECTED_STATUS
from helpers.order_helper import OrderHelper


@allure.epic("API: Orders")
@allure.feature("Order Creation and Retrieval")
class TestOrders:

    @allure.title("Authorized user can create an order")
    @allure.description("Verify that an authenticated user can successfully create an order with valid ingredients.")
    def test_authorized_user_can_create_order(self, authorized_user, default_order_data):
        with allure.step("Send order creation request with authorization token"):
            response = OrderHelper.create_order(default_order_data, token=authorized_user)

        with allure.step("Verify response status code is 200 OK"):
            assert response.status_code == EXPECTED_STATUS.OK

        with allure.step("Verify success=True and order object is present in response"):
            body = response.json()

            assert "success" in body, "Field 'success' is missing from response"
            assert body["success"] is True, "Expected success=True"

            assert "order" in body, "Field 'order' is missing from response"
            assert body["order"] is not None, "Field 'order' is None"

    @allure.title("Unauthorized user can create an order")
    @allure.description("Verify that a guest user can create an order with valid ingredients.")
    def test_unauthorized_user_can_create_order(self, default_order_data):
        with allure.step("Send order creation request without authorization token"):
            response = OrderHelper.create_order(default_order_data)

        with allure.step("Verify response status code is 200 OK"):
            assert response.status_code == EXPECTED_STATUS.OK

        with allure.step("Verify success=True and order object is present in response"):
            body = response.json()

            assert "success" in body, "Field 'success' is missing from response"
            assert body["success"] is True, "Expected success=True"

            assert "order" in body, "Field 'order' is missing from response"
            assert body["order"] is not None, "Field 'order' is None"

    @allure.title("Cannot create an order without ingredients")
    @allure.description("Verify that the server returns 400 Bad Request when no ingredients are provided.")
    def test_cannot_create_order_without_ingredients(self):
        with allure.step("Build an order payload with an empty ingredients list"):
            order_data = {"ingredients": []}

        with allure.step("Send order creation request without ingredients"):
            response = OrderHelper.create_order(order_data)

        with allure.step("Verify response status code is 400 Bad Request"):
            assert response.status_code == EXPECTED_STATUS.BAD_REQUEST

        with allure.step("Verify success=False and error message is present"):
            body = response.json()

            assert "success" in body, "Field 'success' is missing from response"
            assert body["success"] is False, "Expected success=False"

            assert "message" in body, "Field 'message' is missing from response"
            assert body["message"] is not None, "Error message is missing"

    @allure.title("Cannot create an order with an invalid ingredient hash")
    @allure.description("Verify that the server returns an error when an unknown ingredient ID is provided.")
    def test_cannot_create_order_with_invalid_ingredient(self, authorized_user):
        with allure.step("Build an order payload with an invalid ingredient ID"):
            order_data = {"ingredients": ["invalid_ingredient_id"]}

        with allure.step("Send order creation request with invalid ingredient"):
            response = OrderHelper.create_order(order_data, token=authorized_user)

        with allure.step("Verify server returns 500 Internal Server Error (known API behaviour)"):
            assert response.status_code == EXPECTED_STATUS.INTERNAL_SERVER_ERROR

    @allure.title("Authorized user can retrieve their order list")
    @allure.description("Verify that an authenticated user can fetch their order history.")
    def test_authorized_user_can_get_orders(self, authorized_user, default_order_data):
        with allure.step("Create an order to ensure the list is not empty"):
            OrderHelper.create_order(default_order_data, token=authorized_user)

        with allure.step("Send order list request with authorization token"):
            response = OrderHelper.get_orders(token=authorized_user)

        with allure.step("Verify response status code is 200 OK and orders field is a list"):
            assert response.status_code == EXPECTED_STATUS.OK

            body = response.json()
            assert "orders" in body, "Field 'orders' is missing from response"
            assert isinstance(body["orders"], list), "Field 'orders' is not a list"

    @allure.title("Unauthorized user cannot retrieve order list")
    @allure.description("Verify that requesting order history without a token returns 401 Unauthorized.")
    def test_unauthorized_user_cannot_get_orders(self):
        with allure.step("Send order list request without authorization token"):
            response = OrderHelper.get_orders()

        with allure.step("Verify response status code is 401 Unauthorized and error message is present"):
            assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

            body = response.json()
            assert "message" in body, "Field 'message' is missing from response"
            assert body["message"] is not None, "Error message is missing"
