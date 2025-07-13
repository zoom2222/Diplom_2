import pytest
import allure
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
from methods.auth import Auth
from generators import generate_unique_user, get_existing_user


@pytest.fixture
def register_and_delete_user():
    """Фикстура для регистрации пользователя и его удаления после теста"""
    user = generate_unique_user()
    response = Auth.register(user)
    yield response  # передаем ответ в тест

@pytest.fixture
def auth_token():
    """Фикстура для получения токена авторизации"""
    # Сначала регистрируем нового уникального пользователя
    user = generate_unique_user()
    register_response = Auth.register(user)

    # Затем авторизуемся
    login_response = Auth.login({
        "email": user['email'],
        "password": user['password']
    })

    if login_response.status_code != 200:
        pytest.fail(f"Login failed with status {login_response.status_code}")

    token = login_response.json().get('accessToken')

    if not token:
        pytest.fail("Token not found in response")

    yield token

@pytest.fixture(scope="session")
def valid_ingredients():
    """Фикстура для получения валидных ингредиентов (кешируется на всю сессию)"""
    return ["60d3463f7034a000269f45e7", "60d3463f7034a000269f45e9"]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для добавления дополнительной информации в отчет Allure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            # Добавляем в отчет информацию о последнем исключении
            if call.excinfo:
                allure.attach(
                    str(call.excinfo.value),
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT
                )
        except Exception as e:
            print(f"Не удалось добавить информацию в отчет Allure: {e}")