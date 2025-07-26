import pytest
import allure
import sys
import logging
from pathlib import Path

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
from methods.auth import Auth
from generators import generate_unique_user, get_existing_user


@pytest.fixture(scope="module")
def prepared_user():
    """Фикстура для заранее созданного тестового пользователя"""
    user = {
        "email": "prepared_user@example.com",
        "password": "PreparedPass123!",
        "name": "Prepared User"
    }

    # Регистрируем пользователя, если он еще не существует
    register_response = Auth.register(user)
    if register_response.status_code not in [200, 201]:
        # Пробуем авторизоваться, если регистрация не удалась (пользователь уже существует)
        login_response = Auth.login({
            "email": user['email'],
            "password": user['password']
        })
        if login_response.status_code != 200:
            logger.error("Failed to prepare test user")
            pytest.fail("Could not prepare test user")

    logger.info(f"Using prepared user: {user['email']}")
    return user


@pytest.fixture
def register_and_delete_user():
    """Фикстура для регистрации пользователя и его удаления после теста"""
    user = generate_unique_user()
    response = Auth.register(user)
    logger.info(f"Registered new user: {user['email']}")
    return response


@pytest.fixture
def auth_token(prepared_user):
    """Фикстура для получения токена авторизации"""
    # Используем заранее созданного пользователя
    login_response = Auth.login({
        "email": prepared_user['email'],
        "password": prepared_user['password']
    })

    if login_response.status_code != 200:
        logger.error(f"Login failed for prepared user. Status: {login_response.status_code}")
        pytest.fail(f"Login failed with status {login_response.status_code}")

    token = login_response.json().get('accessToken')

    if not token:
        logger.error("Access token not found in login response")
        pytest.fail("Token not found in response")

    logger.info(f"Successfully obtained auth token for prepared user")
    return token


@pytest.fixture(scope="session")
def valid_ingredients():
    """Фикстура для получения валидных ингредиентов (кешируется на всю сессию)"""
    ingredients = ["60d3463f7034a000269f45e7", "60d3463f7034a000269f45e9"]
    logger.info(f"Using valid ingredients: {ingredients}")
    return ingredients


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для добавления дополнительной информации в отчет Allure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if call.excinfo:
                error_msg = str(call.excinfo.value)
                allure.attach(
                    error_msg,
                    name="Ошибка",
                    attachment_type=allure.attachment_type.TEXT
                )
                logger.error(f"Test failed: {error_msg}")
        except Exception as e:
            logger.exception("Failed to add information to Allure report")