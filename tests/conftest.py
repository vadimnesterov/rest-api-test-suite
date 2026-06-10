import pytest
import uuid
from helpers.user_helper import UserHelper
from helpers.order_helper import OrderHelper


# USER FIXTURES

@pytest.fixture
def new_user_data():
    """
    Generate data for a new unique user.

    Uses UserHelper.generate_user() as a base, then replaces the email
    with a guaranteed-unique value to avoid 403 User already exists errors.
    """
    user = UserHelper.generate_user()

    unique = uuid.uuid4().hex[:8]
    user["email"] = f"autotest_{unique}@example.com"

    return user


@pytest.fixture
def created_user(new_user_data):
    """Register a new user before the test and delete the account in teardown."""
    # Register the user before the test
    register_response = UserHelper.register(new_user_data)

    # Verify the user was actually created
    assert register_response.status_code == 200, (
        f"ERROR in fixture: user was NOT created. "
        f"Status: {register_response.status_code}, body: {register_response.text}"
    )

    yield register_response

    # Teardown: delete the user
    login_response = UserHelper.login(new_user_data)
    login_json = login_response.json()
    token = login_json.get("accessToken") or login_json.get("access_token")

    if token:
        UserHelper.delete_user(token)


@pytest.fixture
def authorized_user(new_user_data, created_user):
    """Log in the already registered user and return the access token."""
    login_response = UserHelper.login(new_user_data)
    login_json = login_response.json()
    token = login_json.get("accessToken") or login_json.get("access_token")

    return token


# ORDER FIXTURES

@pytest.fixture
def default_order_data():
    """
    Build a minimal valid order payload.

    Fetches real ingredient IDs from the API and returns:
    {"ingredients": [id1, id2, id3]}
    """
    ingredients_response = OrderHelper.get_ingredients()
    ingredients_json = ingredients_response.json()

    items = ingredients_json.get("data") or []
    ingredient_ids = [item["_id"] for item in items if "_id" in item]

    # Use the first three ingredients if available, otherwise use however many exist
    if len(ingredient_ids) >= 3:
        used_ids = ingredient_ids[:3]
    else:
        used_ids = ingredient_ids

    return {"ingredients": used_ids}


@pytest.fixture
def created_order(authorized_user, default_order_data):
    """
    Create an order on behalf of an authorized user and return the Response.

    Tests can inspect:
    - status_code
    - response body via .json()
    """
    token = authorized_user
    create_response = OrderHelper.create_order(default_order_data, token)

    yield create_response
