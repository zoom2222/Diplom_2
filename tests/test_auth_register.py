import pytest
import allure
from methods.auth import Auth
from generators import generate_unique_user, get_existing_user, get_invalid_user

@allure.epic("API Tests")
@allure.feature("Авторизация")
@allure.story("Регистрация пользователя")
class TestUserRegistration:

    @allure.title("Регистрация уникального пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_register_unique_user(self):
        with allure.step("1. Генерация данных нового пользователя"):
            user = generate_unique_user()
            allure.attach(str(user), name="User data", attachment_type=allure.attachment_type.JSON)

        with allure.step("2. Отправка запроса на регистрацию"):
            response = Auth.register(user)
            allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("3. Проверка ответа"):
            assert response.status_code in [200, 201], f"Неожиданный код ответа: {response.status_code}"
            assert response.json()['success'] is True, "Регистрация не удалась"

    @allure.title("Попытка регистрации существующего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_existing_user(self):
        with allure.step("1. Получение данных существующего пользователя"):
            user = get_existing_user()
            allure.attach(str(user), name="Existing user data", attachment_type=allure.attachment_type.JSON)

        with allure.step("2. Отправка запроса на регистрацию"):
            response = Auth.register(user)
            allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("3. Проверка ошибки"):
            assert response.status_code == 403, f"Неожиданный код ответа: {response.status_code}"
            assert response.json()['message'] == 'User already exists', "Неверное сообщение об ошибке"

    @allure.title("Попытка регистрации с отсутствующим обязательным полем")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_register_missing_field(self, missing_field):
        with allure.step(f"1. Генерация пользователя без поля {missing_field}"):
            user = get_invalid_user(missing_field)
            allure.attach(str(user), name="Invalid user data", attachment_type=allure.attachment_type.JSON)

        with allure.step("2. Отправка запроса на регистрацию"):
            response = Auth.register(user)
            allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("3. Проверка ошибки"):
            assert response.status_code == 403, f"Неожиданный код ответа: {response.status_code}"
            assert 'required fields' in response.json()['message'].lower(), "Неверное сообщение об ошибке"