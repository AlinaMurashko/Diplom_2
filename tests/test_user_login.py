import allure
import pytest
import requests
from data import APIMessages, Fields, HTTPStatus, TestData
from urls import APIEndpoints


@allure.story("Логин пользователя")
class TestUserLogin:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user_success(self, created_user):
        login_data = {
            Fields.EMAIL: created_user[Fields.EMAIL],
            Fields.PASSWORD: created_user[Fields.PASSWORD]
        }

        with allure.step("Отправка запроса на авторизацию с корректными данными"):
            response = requests.post(APIEndpoints.LOGIN, data=login_data)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK

        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert response_data["user"][Fields.EMAIL] == created_user[Fields.EMAIL]
            assert response_data["user"][Fields.NAME] == created_user[Fields.NAME]
            assert "accessToken" in response_data

    @allure.title("Вход с неверным логином или паролем")
    @pytest.mark.parametrize("wrong_field", TestData.LOGIN_FIELDS_TO_TEST)
    def test_login_wrong_credentials_fail(self, created_user, wrong_field):
        login_data = {
            Fields.EMAIL: created_user[Fields.EMAIL],
            Fields.PASSWORD: created_user[Fields.PASSWORD]
        }

        with allure.step(f"Изменение поля {wrong_field} на некорректное значение"):
            login_data[wrong_field] = TestData.WRONG_PREFIX + login_data[wrong_field]

        with allure.step("Отправка запроса с некорректными данными"):
            response = requests.post(APIEndpoints.LOGIN, data=login_data)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.UNAUTHORIZED

        with allure.step("Проверка сообщения об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == APIMessages.INCORRECT_CREDENTIALS