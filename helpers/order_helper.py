import requests
from data import Urls


class OrderHelper:

    @staticmethod
    def create_order(order_data: dict, token: str = None):
        """
        Создать заказ.
        Можно передать токен (для авторизации) или None (заказ без авторизации).
        """
        headers = {}
        if token:
            if not token.startswith("Bearer "):
                token = f"Bearer {token}"
            headers["Authorization"] = token

        return requests.post(
            f"{Urls.BASE_URL}{Urls.ORDERS}",
            json=order_data,
            headers=headers
        )

    @staticmethod
    def cancel_order(track: int):
        """
        Отменить заказ по его номеру (track).
        Ручка: PUT /api/orders/cancel/{track}
        """
        return requests.put(
            f"{Urls.BASE_URL}{Urls.ORDER_CANCEL}{track}"
        )

    @staticmethod
    def get_orders(token: str = None):
        """
        Получить список заказов пользователя.
        Если передать токен — запрос будет авторизованным.
        """
        headers = {}
        if token:
            if not token.startswith("Bearer "):
                token = f"Bearer {token}"
            headers["Authorization"] = token

        return requests.get(
            f"{Urls.BASE_URL}{Urls.ORDERS}",
            headers=headers
        )


    @staticmethod
    def get_ingredients():
        """
        Получить список ингредиентов.
        Используется в тестах для построения валидного заказа.
        """
        return requests.get(
            f"{Urls.BASE_URL}{Urls.INGREDIENTS}"
        )
