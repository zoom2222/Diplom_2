import pytest
import allure
from methods.order import Order

@allure.epic("API Tests")
@allure.feature("Order Management")
@allure.story("Order Creation")
class TestOrderCreation:

    @allure.title("Create order without authorization")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_without_auth(self, valid_ingredients):
        with allure.step("Prepare order data"):
            order_data = {"ingredients": valid_ingredients}
            allure.attach(str(order_data), name="Order Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Send unauthorized order request"):
            response = Order.create(order_data)
            self._attach_response_details(response)

        with allure.step("Verify authorization requirement"):
            assert response.status_code in [401, 403], "Expected unauthorized error"

    @allure.title("Create order with valid ingredients")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_order_with_ingredients(self, auth_token, valid_ingredients):
        with allure.step("Prepare valid order data"):
            order_data = {"ingredients": valid_ingredients}
            allure.attach(str(order_data), name="Order Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Send authorized order request"):
            response = Order.create(order_data, auth_token)
            self._attach_response_details(response)

        with allure.step("Verify successful order creation"):
            assert response.status_code == 200, "Expected success status"
            assert response.json().get('success') is True, "Order creation failed"
            assert 'order' in response.json(), "Order data missing"

    @allure.title("Attempt to create order without ingredients")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_ingredients(self, auth_token):
        with allure.step("Prepare empty order data"):
            order_data = {"ingredients": []}
            allure.attach(str(order_data), name="Empty Order Data", attachment_type=allure.attachment_type.JSON)

        with allure.step("Send invalid order request"):
            response = Order.create(order_data, auth_token)
            self._attach_response_details(response)

        with allure.step("Verify ingredients validation"):
            assert response.status_code == 400, "Expected validation error"
            assert 'provide' in response.json().get('message', '').lower()

    @allure.title("Attempt to create order with invalid ingredients")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_order_with_invalid_ingredients(self, auth_token):
        with allure.step("Prepare order with invalid ingredients"):
            order_data = {"ingredients": ["invalid_hash1", "invalid_hash2"]}
            allure.attach(str(order_data), name="Invalid Ingredients", attachment_type=allure.attachment_type.JSON)

        with allure.step("Send order with invalid data"):
            response = Order.create(order_data, auth_token)
            self._attach_response_details(response)

        with allure.step("Verify ingredients validation"):
            assert response.status_code in [400, 500], "Expected server error"
            assert 'valid' in response.json().get('message', '').lower()

    def _attach_response_details(self, response):
        """Helper method to attach response details"""
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(response.json()), name="Response Body", attachment_type=allure.attachment_type.JSON)
        if hasattr(response, 'request') and response.request.body:
            allure.attach(response.request.body, name="Request Body", attachment_type=allure.attachment_type.JSON)