import random
import requests
import string
from data import Fields
from urls import APIEndpoints

def generate_random_string(length=10):
    """Генерирует случайную строку из букв и цифр."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_payload():
    """Генерирует данные для нового пользователя."""
    email = f"testuser_{generate_random_string(5)}@yandex.ru"
    password = generate_random_string(8)
    name = f"TestUser_{generate_random_string(5)}"

    return {
        Fields.EMAIL: email,
        Fields.PASSWORD: password,
        Fields.NAME: name
    }

def register_user(user_data):
    """Регистрирует пользователя и возвращает ответ."""
    return requests.post(APIEndpoints.REGISTER, data=user_data)

def delete_user(access_token):
    """Удаляет пользователя по токену."""
    headers = {"Authorization": access_token}
    return requests.delete(APIEndpoints.USER, headers=headers)

def login_user(credentials):
    """Авторизует пользователя и возвращает ответ."""
    return requests.post(APIEndpoints.LOGIN, data=credentials)

def create_order(ingredients, access_token=None):
    """Создает заказ с опциональной авторизацией."""
    headers = {"Authorization": access_token} if access_token else {}
    order_data = {"ingredients": ingredients}
    return requests.post(APIEndpoints.ORDERS, json=order_data, headers=headers)

def get_ingredients():
    """Получает список ингредиентов и возвращает ответ."""
    return requests.get(APIEndpoints.INGREDIENTS)
