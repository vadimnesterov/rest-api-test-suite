from faker import Faker

faker = Faker("ru_RU")


class Urls:
    # Базовый URL
    BASE_URL = "https://stellarburgers.education-services.ru"

    # ручки
    REGISTER = "/api/auth/register"
    LOGIN = "/api/auth/login"
    USER = "/api/auth/user"
    ORDERS = "/api/orders"
    INGREDIENTS = "/api/ingredients"
    ORDER_CANCEL = "/api/orders/cancel/"


# Ожидаемые статусы ответа сервера
class EXPECTED_STATUS:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

# Ожидаемые текстовые ответы сервера для негативных сценариев
class ServerResponse:
    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS_MISSING = "Email, password and name are required fields"
    WRONG_CREDENTIALS = "email or password are incorrect"
    UNAUTHORIZED_ORDERS = "You should be authorised"
    SERVER_ERROR = "Internal Server Error"


# Создаем словарь с рандомным валидным пользователем."""
def build_random_user() -> dict:
    return {
        "email": faker.email(),
        "password": faker.password(),
        "name": faker.first_name(),
    }
