import allure

from data import EXPECTED_STATUS
from helpers.order_helper import OrderHelper


@allure.epic("API: Заказы")
@allure.feature("Создание и получение заказов")
class TestOrders:

    @allure.title("Авторизованный пользователь может создать заказ")
    @allure.description("Проверяем, что авторизованный пользователь успешно создаёт заказ с валидными ингредиентами.")
    def test_authorized_user_can_create_order(self, authorized_user, default_order_data):
        with allure.step("Отправить запрос создания заказа с токеном"):
            response = OrderHelper.create_order(default_order_data, token=authorized_user)

        with allure.step("Проверить, что сервер вернул 200 OK"):
            assert response.status_code == EXPECTED_STATUS.OK

        with allure.step("Проверить, что success=True и в ответе присутствует объект заказа"):
            body = response.json()

            success = body.get("success")
            if success is not None:
                assert success is True

            assert body.get("order") is not None

    @allure.title("Неавторизованный пользователь может создать заказ")
    @allure.description("Проверяем, что гость может создать заказ с валидными ингредиентами.")
    def test_unauthorized_user_can_create_order(self, default_order_data):
        with allure.step("Отправить запрос создания заказа без токена"):
            response = OrderHelper.create_order(default_order_data)

        with allure.step("Проверить, что сервер вернул 200 OK"):
            assert response.status_code == EXPECTED_STATUS.OK

        with allure.step("Проверить, что success=True и заказ присутствует в ответе"):
            body = response.json()

            success = body.get("success")
            if success is not None:
                assert success is True

            assert body.get("order") is not None

    @allure.title("Нельзя создать заказ без списка ингредиентов")
    @allure.description("Проверяем, что сервер возвращает 400 Bad Request при отсутствии ингредиентов.")
    def test_cannot_create_order_without_ingredients(self, authorized_user):
        with allure.step("Сформировать заказ с пустым списком ингредиентов"):
            order_data = {"ingredients": []}

        with allure.step("Отправить запрос создания заказа"):
            response = OrderHelper.create_order(order_data, token=authorized_user)

        with allure.step("Проверить, что код ответа — 400 Bad Request"):
            assert response.status_code == EXPECTED_STATUS.BAD_REQUEST

        with allure.step("Проверить, что сервер вернул сообщение об ошибке"):
            body = response.json()

            success = body.get("success")
            if success is not None:
                assert success is False

            assert body.get("message") is not None

    @allure.title("Нельзя создать заказ с невалидным id ингредиента")
    @allure.description("Проверяем, что сервер возвращает ошибку при передаче несуществующего id ингредиента.")
    def test_cannot_create_order_with_invalid_ingredient(self, authorized_user):
        with allure.step("Сформировать заказ с невалидным id ингредиента"):
            order_data = {"ingredients": ["invalid_ingredient_id"]}

        with allure.step("Отправить запрос создания заказа"):
            response = OrderHelper.create_order(order_data, token=authorized_user)

        with allure.step("Проверить известный баг — сервер возвращает 500 Internal Server Error"):
            assert response.status_code == EXPECTED_STATUS.INTERNAL_SERVER_ERROR

    @allure.title("Авторизованный пользователь может получить список своих заказов")
    @allure.description("Проверяем, что пользователь может получить список заказов после авторизации.")
    def test_authorized_user_can_get_orders(self, authorized_user, default_order_data):
        with allure.step("Создать заказ, чтобы список был не пустым"):
            OrderHelper.create_order(default_order_data, token=authorized_user)

        with allure.step("Отправить запрос получения списка заказов с токеном"):
            response = OrderHelper.get_orders(token=authorized_user)

        with allure.step("Проверить, что сервер вернул 200 OK и список заказов — массив"):
            assert response.status_code == EXPECTED_STATUS.OK

            body = response.json()
            assert isinstance(body.get("orders"), list)

    @allure.title("Неавторизованный пользователь не может получить список заказов")
    @allure.description("Проверяем, что запрос списка заказов без токена приводит к 401 Unauthorized.")
    def test_unauthorized_user_cannot_get_orders(self):
        with allure.step("Отправить запрос получения списка заказов без токена"):
            response = OrderHelper.get_orders()

        with allure.step("Проверить, что сервер вернул 401 Unauthorized и сообщение об ошибке"):
            assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

            body = response.json()
            assert body.get("message") is not None
