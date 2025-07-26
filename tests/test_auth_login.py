import pytest
import allure
from methods.auth import Auth
from generators import get_existing_user


@allure.epic("API Тестирование")
@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.story("Успешная авторизация существующего пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Успешный вход с валидными учетными данными")
    def test_login_existing_user(self):
        # Получение тестовых данных
        with allure.step("1. Получение данных существующего пользователя"):
            user = get_existing_user()
            allure.attach(
                str(user),
                name="User credentials",
                attachment_type=allure.attachment_type.JSON
            )

        # Отправка запроса
        with allure.step("2. Отправка запроса авторизации"):
            response = Auth.login({
                "email": user['email'],
                "password": user['password']
            })
            allure.attach(
                str(response.status_code),
                name="Status Code",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                str(response.json()),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверки
        with allure.step("3. Проверка ответа"):
            assert response.status_code == 200, "Неверный код статуса"
            assert response.json()['success'] is True, "Флаг успеха не установлен"
            assert 'accessToken' in response.json(), "Токен доступа отсутствует"

    @allure.story("Неуспешная авторизация с неверными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Попытка входа с невалидными данными: {email}/{password}")
    @pytest.mark.parametrize('email,password', [
        ('wrong@email.com', 'password123'),
        ('test@example.com', 'wrongpassword'),
        ('', 'password123'),
        ('test@example.com', '')
    ])
    def test_login_invalid_credentials(self, email, password):
        # Подготовка данных
        with allure.step("1. Подготовка невалидных учетных данных"):
            credentials = {
                "email": email,
                "password": password
            }
            allure.attach(
                str(credentials),
                name="Invalid credentials",
                attachment_type=allure.attachment_type.JSON
            )

        # Отправка запроса
        with allure.step("2. Отправка запроса с невалидными данными"):
            response = Auth.login(credentials)
            allure.attach(
                str(response.status_code),
                name="Status Code",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                str(response.json()),
                name="Error Response",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверки
        with allure.step("3. Проверка ошибки авторизации"):
            assert response.status_code == 401, "Ожидался код 401 Unauthorized"
            assert 'email or password are incorrect' in response.json().get('message', ''), \
                "Неверное сообщение об ошибке"