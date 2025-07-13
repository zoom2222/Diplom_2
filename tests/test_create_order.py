import pytest
import allure
from methods.order import Order

@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.story("Создание заказа с авторизацией")
    def test_create_order_without_auth(self, valid_ingredients):
        response = Order.create({
            "ingredients": valid_ingredients
        })
        # Ожидаем либо 401 (Unauthorized), либо 400 (Bad Request)
        assert response.status_code in [400, 401], f"Unexpected status code: {response.status_code}"

    @allure.story("Создание заказа без авторизации")
    def test_create_order_without_auth(self, valid_ingredients):
        response = Order.create({
            "ingredients": valid_ingredients
        })
        assert response.status_code == 200  # или 401, зависит от API

    @allure.story("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, auth_token, valid_ingredients):
        response = Order.create({
            "ingredients": valid_ingredients
        }, auth_token)
        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.story("Попытка создания заказа без ингредиентов")
    def test_create_order_without_ingredients(self, auth_token):
        response = Order.create({
            "ingredients": []
        }, auth_token)
        assert response.status_code == 400
        assert 'must be provided' in response.json()['message']

    @allure.story("Попытка создания заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients(self, auth_token):
        response = Order.create({
            "ingredients": ["invalid_hash1", "invalid_hash2"]
        }, auth_token)
        assert response.status_code == 500
