import pytest

from helpers.user_helper import UserHelper
from helpers.order_helper import OrderHelper


# ПОЛЬЗОВАТЕЛЬ

@pytest.fixture
def new_user_data():

    # Генерируем данные нового пользователя.

    return UserHelper.generate_user()


@pytest.fixture
def created_user(new_user_data):

    # Регистрируем пользователя перед тестом и возвращаем Response.

    register_response = UserHelper.register(new_user_data)

    # Отдаём сам Response в тест
    yield register_response

    # После теста пробуем залогиниться и удалить пользователя
    login_response = UserHelper.login(new_user_data)
    login_json = login_response.json()
    token = login_json.get("accessToken") or login_json.get("access_token")

    if token:
        UserHelper.delete_user(token)


@pytest.fixture
def authorized_user(new_user_data, created_user):

    # Логиним уже зарегистрированного пользователя и возвращает только токен(строку).

    login_response = UserHelper.login(new_user_data)
    login_json = login_response.json()
    token = login_json.get("accessToken") or login_json.get("access_token")
    return token


# ЗАКАЗ

@pytest.fixture
def default_order_data():
    """
    Строим простое валидное тело заказа.

    Ингредиенты из API и возвращаем:
    {"ingredients": [id1, id2, id3]}
    """
    ingredients_response = OrderHelper.get_ingredients()
    ingredients_json = ingredients_response.json()

    items = ingredients_json.get("data") or []
    ingredient_ids = [item["_id"] for item in items if "_id" in item]

    # Если ингредиентов много — берём первые несколько,
    # если мало — используем сколько есть.
    if len(ingredient_ids) >= 3:
        used_ids = ingredient_ids[:3]
    else:
        used_ids = ingredient_ids

    return {"ingredients": used_ids}


@pytest.fixture
def created_order(authorized_user, default_order_data):
    """
    Создаём заказ от имени авторизованного пользователя и возвращаем Response.

    В тесте можно проверять:
    - status_code
    - тело через .json()
    """
    token = authorized_user
    create_response = OrderHelper.create_order(default_order_data, token)

    # Отдаём Response в тест
    yield create_response

    # Если можно — отменяем заказ, если API вернул track
    try:
        order_json = create_response.json()
    except ValueError:
        order_json = {}

    track = order_json.get("track")
    if track:
        OrderHelper.cancel_order(track)
