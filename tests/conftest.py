import allure
import pytest
from data import Fields
from helpers import delete_user, generate_user_payload, get_ingredients, register_user

@pytest.fixture
def registered_user():
    """
    Фикстура создает пользователя, возвращает его данные и токен,
    а после теста удаляет его.
    """
    user_payload = generate_user_payload()
    with allure.step(f"Создание пользователя с email: {user_payload[Fields.EMAIL]}"):
        response = register_user(user_payload)
        response_data = response.json()
        user_payload[Fields.ACCESS_TOKEN] = response_data.get("accessToken")

    yield user_payload

    access_token = user_payload.get(Fields.ACCESS_TOKEN)
    if access_token:
        with allure.step(f"Удаление пользователя с email: {user_payload[Fields.EMAIL]}"):
            delete_user(access_token)

@pytest.fixture
def ingredients_list():
    """Фикстура возвращает список актуальных хешей ингредиентов."""
    with allure.step("Получение списка доступных ингредиентов"):
        response = get_ingredients()
        ingredients_data = response.json()

    ingredients_ids = [ingredient["_id"] for ingredient in ingredients_data.get("data", [])]

    with allure.step(f"Получено {len(ingredients_ids)} ингредиентов"):
        return ingredients_ids
