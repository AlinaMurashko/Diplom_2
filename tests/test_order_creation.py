import allure
from data import APIMessages, Fields, HTTPStatus, TestData
from helpers import create_order

@allure.story("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_auth_with_ingredients_success(self, registered_user, ingredients_list):
        with allure.step("Отправка запроса на создание заказа с авторизацией"):
            response = create_order(ingredients_list, registered_user[Fields.ACCESS_TOKEN])

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK

        with allure.step("Проверка структуры и содержимого ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert Fields.NAME in response_data
            assert "order" in response_data

        with allure.step("Проверка соответствия ингредиентов в заказе"):
            response_ingredients = [ingredient["_id"] for ingredient in response_data["order"]["ingredients"]]
            assert ingredients_list == response_ingredients

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauth_with_ingredients_success(self, ingredients_list):
        with allure.step("Отправка запроса на создание заказа без авторизации"):
            response = create_order(ingredients_list)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK

        with allure.step("Проверка структуры ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert Fields.NAME in response_data
            assert "order" in response_data

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_fail(self, registered_user):
        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            response = create_order([], registered_user[Fields.ACCESS_TOKEN])

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.BAD_REQUEST

        with allure.step("Проверка сообщения об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == APIMessages.INGREDIENTS_REQUIRED

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash_fail(self, registered_user):
        with allure.step("Отправка запроса с невалидным хешем ингредиента"):
            response = create_order([TestData.INVALID_INGREDIENT_HASH], registered_user[Fields.ACCESS_TOKEN])

        with allure.step("Проверка статус-кода ответа (ожидается 500 Internal Server Error)"):
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
