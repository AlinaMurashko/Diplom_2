import allure
import pytest
import requests
from data import APIMessages, Fields, HTTPStatus, TestData
from urls import APIEndpoints


@allure.story("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_payload):
        with allure.step("Отправка запроса на регистрацию нового пользователя"):
            response = requests.post(APIEndpoints.REGISTER, data=user_payload)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK

        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert response_data["user"][Fields.EMAIL] == user_payload[Fields.EMAIL]
            assert response_data["user"][Fields.NAME] == user_payload[Fields.NAME]
            assert "accessToken" in response_data

    @allure.title("Невозможно создать пользователя, который уже существует")
    def test_create_existing_user_fail(self, created_user):
        existing_user_data = {
            Fields.EMAIL: created_user[Fields.EMAIL],
            Fields.PASSWORD: created_user[Fields.PASSWORD],
            Fields.NAME: created_user[Fields.NAME]
        }

        with allure.step("Отправка запроса на регистрацию уже существующего пользователя"):
            response = requests.post(APIEndpoints.REGISTER, data=existing_user_data)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.FORBIDDEN

        with allure.step("Проверка сообщения об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == APIMessages.USER_EXISTS

    @allure.title("Невозможно создать пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("missing_field", TestData.REQUIRED_USER_FIELDS)
    def test_create_user_missing_field_fail(self, user_payload, missing_field):
        with allure.step(f"Удаление обязательного поля {missing_field} из запроса"):
            del user_payload[missing_field]

        with allure.step("Отправка запроса с отсутствующим полем"):
            response = requests.post(APIEndpoints.REGISTER, data=user_payload)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.FORBIDDEN

        with allure.step("Проверка сообщения об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == APIMessages.REQUIRED_FIELDS
