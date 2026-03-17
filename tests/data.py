class APIMessages:
    USER_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INCORRECT_CREDENTIALS = "email or password are incorrect"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"
    UNAUTHORIZED = "You should be authorised"

class HTTPStatus:
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

class Fields:
    EMAIL = "email"
    NAME = "name"
    PASSWORD = "password"
    ACCESS_TOKEN = "access_token"

class TestData:
    REQUIRED_USER_FIELDS = [Fields.EMAIL, Fields.PASSWORD, Fields.NAME]
    LOGIN_FIELDS_TO_TEST = [Fields.EMAIL, Fields.PASSWORD]

    INVALID_INGREDIENT_HASH = "invalid_ingredient_id_12345"
    WRONG_PREFIX = "wrong_"
