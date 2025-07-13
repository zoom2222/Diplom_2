import pytest
import allure
from methods.auth import Auth
from generators import get_existing_user

@allure.feature("Авторизация пользователя")
class TestUserLogin:
    @allure.story("Успешная авторизация существующего пользователя")
    class TestUserLogin:
        def test_login_existing_user(self):
            user = get_existing_user()  # Используем реальные тестовые данные
            response = Auth.login({
                "email": user['email'],
                "password": user['password']
            })
            assert response.status_code == 200
            assert response.json()['success'] is True
            assert 'accessToken' in response.json()

    @allure.story("Неуспешная авторизация с неверными данными")
    @pytest.mark.parametrize('email,password', [
        ('wrong@email.com', 'password123'),
        ('test@example.com', 'wrongpassword'),
        ('', 'password123'),
        ('test@example.com', '')
    ])
    def test_login_invalid_credentials(self, email, password):
        response = Auth.login({
            "email": email,
            "password": password
        })
        assert response.status_code == 401
        assert response.json()['message'] == 'email or password are incorrect'
