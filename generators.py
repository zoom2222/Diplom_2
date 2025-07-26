from faker import Faker

fake = Faker()

def generate_unique_user():
    return {
        "email": fake.unique.email(),
        "password": fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
        "name": fake.name()
    }

def get_existing_user():
    return {
        "email": "test@example.com",  # Замените на реальные тестовые данные
        "password": "password123",
        "name": "Test User"
    }

def get_invalid_user(missing_field=None):
    """Генерирует пользователя с отсутствующим полем или пустыми значениями"""
    user = {
        "email": "invalid@example.com",
        "password": "short",
        "name": ""
    }
    if missing_field:
        user.pop(missing_field)
    return user