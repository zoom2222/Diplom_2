class Url:
    BASE_URL = 'https://stellarburgers.nomoreparties.site/api'
    AUTH_URL = '/auth'
    ORDERS_URL = '/orders'


class DataForAuth:
    REGISTER_BODY = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }

    LOGIN_BODY = {
        "email": "test@example.com",
        "password": "password123"
    }


class DataForOrder:
    CREATE_ORDER_BODY = {
        "ingredients": ["60d3463f7034a000269f45e7", "60d3463f7034a000269f45e9"]
    }
