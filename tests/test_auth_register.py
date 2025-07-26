import pytest
import allure
from methods.auth import Auth
from generators import generate_unique_user, get_invalid_user

@allure.epic("API Tests")
@allure.feature("User Management")
@allure.story("User Registration")
class TestUserRegistration:

    @allure.title("Successful registration of new user")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_register_unique_user(self):
        """Тест регистрации нового уникального пользователя"""
        with allure.step("Generate unique user data"):
            user = generate_unique_user()
            allure.attach(str(user), name="User Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Send registration request"):
            response = Auth.register(user)
            allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.json()), name="Response Body", attachment_type=allure.attachment_type.JSON)

        with allure.step("Verify successful registration"):
            assert response.status_code in [200, 201], "Unexpected status code"
            assert response.json()['success'] is True, "Registration failed"

    @allure.title("Attempt to register existing user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_existing_user(self, prepared_user):
        """Тест попытки регистрации уже существующего пользователя"""
        with allure.step("Get prepared user credentials"):
            allure.attach(str(prepared_user), name="Existing User Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Send duplicate registration request"):
            response = Auth.register(prepared_user)
            allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.json()), name="Error Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("Verify duplicate user error"):
            assert response.status_code == 403, "Expected 403 Forbidden"
            assert 'already exists' in response.json().get('message', '').lower()

    @allure.title("Registration with missing required field: {missing_field}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_register_missing_field(self, missing_field):
        """Тест регистрации с отсутствующим обязательным полем"""
        with allure.step(f"Create user without '{missing_field}' field"):
            user = get_invalid_user(missing_field)
            allure.attach(str(user), name="Invalid User Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Send invalid registration request"):
            response = Auth.register(user)
            allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.json()), name="Error Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("Verify validation error"):
            assert response.status_code == 403, "Expected validation error"
            assert 'required' in response.json().get('message', '').lower()