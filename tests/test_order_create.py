import pytest
import allure

from data import EXPECTED_STATUS
from helpers.order_helper import OrderHelper


def test_authorized_user_can_create_order(authorized_user, default_order_data):
    """
    Позитивный сценарий:
    авторизованный пользователь может создать заказ.
    """
    # Создаём заказ с токеном авторизованного пользователя
    response = OrderHelper.create_order(default_order_data, token=authorized_user)

    # Проверяем статус-код (200 OK — заказ успешно создан)
    assert response.status_code == EXPECTED_STATUS.OK

    # Проверяем тело ответа
    body = response.json()

    success = body.get("success")
    if success is not None:
        assert success is True

    # В ответе должен быть объект заказа (номер заказа и т.п.)
    order = body.get("order")
    assert order is not None


def test_unauthorized_user_can_create_order(default_order_data):
    """
    Позитивный сценарий:
    неавторизованный пользователь тоже может создать заказ.
    """
    # Создаём заказ без токена
    response = OrderHelper.create_order(default_order_data)

    # Проверяем статус-код (200 OK — заказ создан без авторизации)
    assert response.status_code == EXPECTED_STATUS.OK

    # Проверяем тело ответа
    body = response.json()

    success = body.get("success")
    if success is not None:
        assert success is True

    # В ответе должен быть объект заказа
    assert body.get("order") is not None


def test_cannot_create_order_without_ingredients(authorized_user):
    """
    Негативный сценарий:
    нельзя создать заказ без списка ингредиентов.
    """
    # Пустой список ингредиентов
    order_data = {"ingredients": []}

    # Пытаемся создать заказ с пустым списком ингредиентов
    response = OrderHelper.create_order(order_data, token=authorized_user)

    # Ожидаем 400 Bad Request — некорректные данные запроса
    assert response.status_code == EXPECTED_STATUS.BAD_REQUEST

    # Проверяем тело ответа
    body = response.json()

    success = body.get("success")
    if success is not None:
        assert success is False

    # В ответе должно быть понятное сообщение об ошибке
    assert body.get("message") is not None


def test_cannot_create_order_with_invalid_ingredient(authorized_user):
    """
    Негативный сценарий:
    нельзя создать заказ с невалидным id ингредиента.
    """
    # Заведомо несуществующий id ингредиента
    order_data = {"ingredients": ["invalid_ingredient_id"]}

    # Пытаемся создать заказ с невалидным ингредиентом
    response = OrderHelper.create_order(order_data, token=authorized_user)

    # Для этого кейса известен баг: сервер может возвращать 500.
    # Ожидаем внутреннюю ошибку сервера.
    assert response.status_code == EXPECTED_STATUS.INTERNAL_SERVER_ERROR


def test_authorized_user_can_get_orders(authorized_user, default_order_data):
    """
    Позитивный сценарий:
    авторизованный пользователь может получить список своих заказов.
    """
    # На всякий случай создаём заказ, чтобы список точно был не пустым
    OrderHelper.create_order(default_order_data, token=authorized_user)

    # Получаем список заказов авторизованного пользователя
    response = OrderHelper.get_orders(token=authorized_user)

    # Проверяем статус-код (200 OK — список заказов успешно получен)
    assert response.status_code == EXPECTED_STATUS.OK

    # Проверяем тело ответа
    body = response.json()

    orders = body.get("orders")
    # Ожидаем, что сервер вернёт список заказов
    assert isinstance(orders, list)


def test_unauthorized_user_cannot_get_orders():
    """
    Негативный сценарий:
    неавторизованный пользователь не может получить список заказов.
    """
    # Пытаемся получить список заказов без токена
    response = OrderHelper.get_orders()

    # Ожидаем 401 Unauthorized — доступ разрешён только авторизованным пользователям
    assert response.status_code == EXPECTED_STATUS.UNAUTHORIZED

    # Проверяем тело ответа
    body = response.json()

    # Проверяем, что сервер вернул сообщение об ошибке
    assert body.get("message") is not None


