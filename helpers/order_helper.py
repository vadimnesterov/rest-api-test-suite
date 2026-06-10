import requests
from data import Urls


class OrderHelper:

    @staticmethod
    def create_order(order_data: dict, token: str = None):
        """POST /api/orders — create an order. Pass a token for an authenticated request."""
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
    def get_orders(token: str = None):
        """GET /api/orders — get the user's order list. Pass a token for an authenticated request."""
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
        """GET /api/ingredients — fetch the ingredient list for building valid order payloads."""
        return requests.get(
            f"{Urls.BASE_URL}{Urls.INGREDIENTS}"
        )
