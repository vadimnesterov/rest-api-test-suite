# version: v1.1


# --- БАЗОВЫЕ НАСТРОЙКИ СТЕНДА ---

class BaseUrls:
    """Базовые адреса стендов"""
    BASE_URL = "https://stellarburgers.education-services.ru"


# --- ОТНОСИТЕЛЬНЫЕ API-ПУТИ (НЕ ЗАВИСЯТ ОТ СТЕНДА) ---

class ApiPaths:
    REGISTER = "/api/auth/register"
    LOGIN = "/api/auth/login"
    USER = "/api/auth/user"
    ORDERS = "/api/orders"
    INGREDIENTS = "/api/ingredients"
    ORDER_CANCEL = "/api/orders/cancel/"


# --- ПОЛНЫЕ API-URL (КОНКАТЕНАЦИЯ) ---

class ApiUrls:
    REGISTER = BaseUrls.BASE_URL + ApiPaths.REGISTER
    LOGIN = BaseUrls.BASE_URL + ApiPaths.LOGIN
    USER = BaseUrls.BASE_URL + ApiPaths.USER
    ORDERS = BaseUrls.BASE_URL + ApiPaths.ORDERS
    INGREDIENTS = BaseUrls.BASE_URL + ApiPaths.INGREDIENTS
    ORDER_CANCEL = BaseUrls.BASE_URL + ApiPaths.ORDER_CANCEL


# --- ОБРАТНАЯ СОВМЕСТИМОСТЬ (ЧТОБЫ НЕ ЛОМАТЬ ПРОЕКТ) ---

class Urls:
    """
    Оставлен для совместимости со старым кодом.
    Можно постепенно переводить проект на ApiUrls.
    """
    BASE_URL = BaseUrls.BASE_URL

    REGISTER = ApiPaths.REGISTER
    LOGIN = ApiPaths.LOGIN
    USER = ApiPaths.USER
    ORDERS = ApiPaths.ORDERS
    INGREDIENTS = ApiPaths.INGREDIENTS
    ORDER_CANCEL = ApiPaths.ORDER_CANCEL


# --- ОЖИДАЕМЫЕ СТАТУСЫ ОТВЕТОВ СЕРВЕРА ---

class EXPECTED_STATUS:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


# --- ТЕКСТОВЫЕ ОТВЕТЫ СЕРВЕРА ДЛЯ НЕГАТИВНЫХ СЦЕНАРИЕВ ---

class ServerResponse:
    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS_MISSING = "Email, password and name are required fields"
    WRONG_CREDENTIALS = "email or password are incorrect"
    UNAUTHORIZED_ORDERS = "You should be authorised"
    SERVER_ERROR = "Internal Server Error"
