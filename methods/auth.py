import pytest
import requests

from data import Url


class Auth:
    @staticmethod
    def register(body):
        try:
            response = requests.post(Url.BASE_URL + Url.AUTH_URL + '/register', json=body)
            return response
        except Exception as e:
            pytest.fail(f"Registration request failed: {str(e)}")

    @staticmethod
    def login(body):
        try:
            response = requests.post(Url.BASE_URL + Url.AUTH_URL + '/login', json=body)
            return response
        except Exception as e:
            pytest.fail(f"Login request failed: {str(e)}")
