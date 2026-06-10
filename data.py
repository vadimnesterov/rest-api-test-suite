# --- BASE ENVIRONMENT SETTINGS ---

class BaseUrls:
    """Base environment URLs."""
    BASE_URL = "https://stellarburgers.education-services.ru"


# --- RELATIVE API PATHS (ENVIRONMENT-INDEPENDENT) ---

class ApiPaths:
    REGISTER = "/api/auth/register"
    LOGIN = "/api/auth/login"
    USER = "/api/auth/user"
    ORDERS = "/api/orders"
    INGREDIENTS = "/api/ingredients"


# --- FULL API URLS (BASE + PATH) ---

class ApiUrls:
    REGISTER = BaseUrls.BASE_URL + ApiPaths.REGISTER
    LOGIN = BaseUrls.BASE_URL + ApiPaths.LOGIN
    USER = BaseUrls.BASE_URL + ApiPaths.USER
    ORDERS = BaseUrls.BASE_URL + ApiPaths.ORDERS
    INGREDIENTS = BaseUrls.BASE_URL + ApiPaths.INGREDIENTS


# --- BACKWARD COMPATIBILITY SHIM ---

class Urls:
    """Kept for compatibility with existing helper code."""
    BASE_URL = BaseUrls.BASE_URL

    REGISTER = ApiPaths.REGISTER
    LOGIN = ApiPaths.LOGIN
    USER = ApiPaths.USER
    ORDERS = ApiPaths.ORDERS
    INGREDIENTS = ApiPaths.INGREDIENTS


# --- EXPECTED HTTP STATUS CODES ---

class EXPECTED_STATUS:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


# --- EXPECTED SERVER ERROR MESSAGES ---

class ServerResponse:
    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS_MISSING = "Email, password and name are required fields"
    WRONG_CREDENTIALS = "email or password are incorrect"
    UNAUTHORIZED_ORDERS = "You should be authorised"
    SERVER_ERROR = "Internal Server Error"
