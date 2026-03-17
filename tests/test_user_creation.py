import allure
import pytest
from data import APIMessages, Fields, HTTPStatus, TestData
from helpers import delete_user, generate_user_payload, register_user

@allure.story("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self):
        with allure.step("Генерация данных нового пользователя"):
            user_data = generate_user_payload()

        with allure.step("Отправка запроса на регистрацию"):
            response = register_user(user_data)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK

        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert response_data["user"][Fields.EMAIL] == user_data[Fields.EMAIL]
            assert response_data["user"][Fields.NAME] == user_data[Fields.NAME]
            assert "accessToken" in response_data

    @allure.title("Невозможно создать пользователя, который уже существует")
    def test_create_existing_user_fail(self, registered_user):
        with allure.step("Попытка повторной регистрации того же пользователя"):
            response = register_user(registered_user)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.FORBIDDEN

        with allure.step("Проверка сообщения об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == APIMessages.USER_EXISTS

    @allure.title("Невозможно создать пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("missing_field", TestData.REQUIRED_USER_FIELDS)
    def test_create_user_missing_field_fail(self, missing_field):
        with allure.step("Генерация данных пользователя"):
            user_data = generate_user_payload()

        with allure.step(f"Удаление обязательного поля {missing_field} из запроса"):
            del user_data[missing_field]

        with allure.step("Отправка запроса с отсутствующим полем"):
            response = register_user(user_data)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.FORBIDDEN

        with allure.step("Проверка сообщения об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == APIMessages.REQUIRED_FIELDS
