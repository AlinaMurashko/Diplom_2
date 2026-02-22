import allure
import pytest
import requests
from data import HTTPStatus, Fields
from urls import APIEndpoints
from helpers import generate_random_string


@pytest.fixture
def user_payload():
    """
    Фикстура генерирует данные для нового пользователя.
    Возвращает словарь с данными нового пользователя.
    """
    email = f"testuser_{generate_random_string(5)}@yandex.ru"
    password = generate_random_string(8)
    name = f"TestUser_{generate_random_string(5)}"

    with allure.step(f"Генерация данных пользователя: email={email}, name={name}"):
        return {
            Fields.EMAIL: email,
            Fields.PASSWORD: password,
            Fields.NAME: name
        }


@pytest.fixture
def created_user(user_payload):
    """
    Фикстура создает пользователя, возвращает его данные и токен,
    а после теста удаляет его.
    """
    with allure.step(f"Создание пользователя с email: {user_payload[Fields.EMAIL]}"):
        response = requests.post(APIEndpoints.REGISTER, data=user_payload)
        response_data = response.json()

    user_payload["access_token"] = response_data.get("accessToken")

    yield user_payload

    if user_payload["access_token"]:
        with allure.step(f"Удаление пользователя с email: {user_payload[Fields.EMAIL]}"):
            headers = {"Authorization": user_payload["access_token"]}
            response = requests.delete(APIEndpoints.USER, headers=headers)
            assert response.status_code == HTTPStatus.ACCEPTED


@pytest.fixture
def ingredients_list():
    """Фикстура возвращает список актуальных хешей ингредиентов."""
    with allure.step("Получение списка доступных ингредиентов"):
        response = requests.get(APIEndpoints.INGREDIENTS)
        ingredients_data = response.json()

    ingredients_ids = [ingredient["_id"] for ingredient in ingredients_data.get("data", [])]

    with allure.step(f"Получено {len(ingredients_ids)} ингредиентов"):
        return ingredients_ids
