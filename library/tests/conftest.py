import pytest
from django.urls import reverse


# Базовые пользователи

@pytest.fixture
def user_data():
    """Словарь с данными для нового пользователя (используется в формах)."""
    return {
        "username": "testuser",
        "first_name": "Иван",
        "last_name": "Иванов",
        "email": "ivan@example.com",
        "phone": "+7-900-000-00-00",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
        "role": "student",
    }


@pytest.fixture
def create_user(db):
    """
    Фабрика пользователей.
    Использование:
        user = create_user(username='alice', email='alice@test.com')
    """
    from users.models import CustomUser

    def _make(username="alice", email=None, password="TestPass123!", **kwargs):
        email = email or f"{username}@test.com"
        return CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=kwargs.pop("first_name", "Имя"),
            last_name=kwargs.pop("last_name", "Фамилия"),
            **kwargs,
        )

    return _make


@pytest.fixture
def alice(create_user):
    """Готовый пользователь alice."""
    return create_user(username="alice", email="alice@test.com")


@pytest.fixture
def bob(create_user):
    """Готовый пользователь bob."""
    return create_user(username="bob", email="bob@test.com")


@pytest.fixture
def charlie(create_user):
    """Готовый пользователь charlie (незнакомец)."""
    return create_user(username="charlie", email="charlie@test.com")


@pytest.fixture
def admin_user(create_user):
    """Суперпользователь."""
    return create_user(
        username="admin",
        email="admin@test.com",
        password="AdminPass123!",
        is_staff=True,
        is_superuser=True,
        role="admin",
    )


# Клиенты

@pytest.fixture
def anon_client(client):
    """Анонимный клиент (без логина). Просто псевдоним для читаемости."""
    return client


@pytest.fixture
def auth_client(client, alice):
    """Клиент, залогиненный как alice."""
    client.force_login(alice)
    return client


@pytest.fixture
def bob_client(client, bob):
    """Клиент, залогиненный как bob."""
    client.force_login(bob)
    return client


# Состояния соцсети

@pytest.fixture
def alice_and_bob_friends(alice, bob):
    """alice и bob уже друзья."""
    alice.friends.add(bob)
    return alice, bob


@pytest.fixture
def alice_sent_request_to_bob(alice, bob):
    """alice отправила заявку bob."""
    alice.friend_requests.add(bob)
    return alice, bob


# URL-хелперы

@pytest.fixture
def urls():
    """Словарь часто используемых URL для удобства."""
    return {
        "register":    reverse("users:register"),
        "login":       reverse("login"),
        "logout":      reverse("logout"),
        "user_list":   reverse("users:user_list"),
        "profile_edit": reverse("users:profile_edit"),
    }
