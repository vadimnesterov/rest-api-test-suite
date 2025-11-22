import pytest

from data import EXPECTED_STATUS
from helpers.user_helper import UserHelper


def test_user_can_be_created_successfully(new_user_data):
    """
    Позитивный сценарий:
    новый уникальный пользователь может быть успешно создан.
    """
    response = UserHelper.register(new_user_data)

    assert response.status_code == EXPECTED_STATUS.OK

    body = response.json()

    success = body.get("success")
    if success is not None:
        assert success is True

    assert body.get("accessToken") is not None


def test_cannot_create_user_that_already_exists(new_user_data, created_user):
    """
    Негативный сценарий:
    нельзя создать пользователя, который уже зарегистрирован.
    """
    response = UserHelper.register(new_user_data)

    assert response.status_code == EXPECTED_STATUS.FORBIDDEN

    body = response.json()

    success = body.get("success")
    if success is not None:
        assert success is False

    assert body.get("message") is not None


@pytest.mark.parametrize(
    "field_to_remove",
    ["email", "password", "name"],
)
def test_cannot_create_user_without_required_field(new_user_data, field_to_remove):
    """
    Негативный сценарий:
    нельзя создать пользователя, если не заполнено одно из обязательных полей.
    """
    invalid_data = new_user_data.copy()
    invalid_data.pop(field_to_remove, None)

    response = UserHelper.register(invalid_data)

    assert response.status_code == EXPECTED_STATUS.FORBIDDEN

    body = response.json()

    success = body.get("success")
    if success is not None:
        assert success is False

    assert body.get("message") is not None
