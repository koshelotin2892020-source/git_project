import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from users.forms import CustomUserCreationForm, ProfileEditForm
from users.models import CustomUser


# 1. РЕГИСТРАЦИЯ

@pytest.mark.django_db
class TestRegistration:
    """Тесты страницы и логики регистрации."""

    def test_register_page_loads(self, anon_client, urls):
        """GET /auth/register/ отдаёт 200 и форму регистрации."""
        response = anon_client.get(urls["register"])
        assert response.status_code == 200
        assert "form" in response.context
        assert isinstance(response.context["form"], CustomUserCreationForm)

    def test_register_success(self, anon_client, user_data, urls):
        """Успешная регистрация создаёт пользователя и делает редирект на профиль."""
        response = anon_client.post(urls["register"], data=user_data)
        assert CustomUser.objects.filter(username=user_data["username"]).exists()
        assert response.status_code == 302
        assert reverse("users:profile", kwargs={"username": user_data["username"]}) in response["Location"]

    def test_register_autologin(self, anon_client, user_data, urls):
        """После регистрации пользователь автоматически залогинен."""
        anon_client.post(urls["register"], data=user_data)
        profile_url = reverse("users:profile", kwargs={"username": user_data["username"]})
        response = anon_client.get(profile_url)
        assert response.status_code == 200

    def test_register_phone_saved(self, anon_client, user_data, urls):
        """Номер телефона сохраняется при регистрации."""
        anon_client.post(urls["register"], data=user_data)
        user = CustomUser.objects.get(username=user_data["username"])
        assert user.phone == user_data["phone"]

    def test_register_email_saved(self, anon_client, user_data, urls):
        """Email сохраняется при регистрации."""
        anon_client.post(urls["register"], data=user_data)
        user = CustomUser.objects.get(username=user_data["username"])
        assert user.email == user_data["email"]

    def test_register_duplicate_username(self, anon_client, alice, user_data, urls):
        """Повторный username вызывает ошибку формы."""
        user_data["username"] = alice.username
        user_data["email"] = "another@test.com"
        response = anon_client.post(urls["register"], data=user_data)
        assert response.status_code == 200
        assert CustomUser.objects.filter(email="another@test.com").count() == 0

    def test_register_duplicate_email(self, anon_client, alice, user_data, urls):
        """Повторный email вызывает ошибку формы."""
        user_data["email"] = alice.email
        response = anon_client.post(urls["register"], data=user_data)
        assert response.status_code == 200
        form = response.context["form"]
        assert "email" in form.errors

    def test_register_authenticated_user_redirected(self, auth_client, alice, urls):
        """Залогиненный пользователь перенаправляется со страницы регистрации."""
        response = auth_client.get(urls["register"])
        assert response.status_code == 302
        assert alice.username in response["Location"]

    @pytest.mark.parametrize("missing_field", [
        "username", "email", "first_name", "last_name", "password1", "password2",
    ])
    def test_register_required_fields(self, anon_client, user_data, urls, missing_field):
        """Отсутствие любого обязательного поля — форма невалидна."""
        user_data[missing_field] = ""
        response = anon_client.post(urls["register"], data=user_data)
        assert response.status_code == 200
        assert not CustomUser.objects.filter(username=user_data.get("username", "")).exists()

    @pytest.mark.parametrize("bad_email", [
        "notanemail",
        "missing@",
        "@nodomain.com",
        "spaces in@email.com",
    ])
    def test_register_invalid_email(self, anon_client, user_data, urls, bad_email):
        """Невалидный email — форма не принята."""
        user_data["email"] = bad_email
        response = anon_client.post(urls["register"], data=user_data)
        assert response.status_code == 200
        assert not CustomUser.objects.filter(username=user_data["username"]).exists()

    @pytest.mark.parametrize("password,confirm", [
        ("short1!", "short1!"),
        ("StrongPass123!", "WrongPass!"),
        ("password", "password"),
        ("12345678", "12345678"),
    ])
    def test_register_bad_passwords(self, anon_client, user_data, urls, password, confirm):
        """Невалидный пароль — форма не принята."""
        user_data["password1"] = password
        user_data["password2"] = confirm
        response = anon_client.post(urls["register"], data=user_data)
        assert response.status_code == 200
        assert not CustomUser.objects.filter(username=user_data["username"]).exists()


# 2. ВХОД / ВЫХОД

@pytest.mark.django_db
class TestLoginLogout:
    """Тесты входа и выхода из системы."""

    def test_login_page_loads(self, anon_client, urls):
        """GET /auth/login/ возвращает 200."""
        response = anon_client.get(urls["login"])
        assert response.status_code == 200

    def test_login_success(self, anon_client, alice, urls):
        """Успешный вход с правильными данными."""
        response = anon_client.post(urls["login"], {
            "username": alice.username,
            "password": "TestPass123!",
        })
        assert response.status_code == 302

    def test_login_redirects_to_next(self, anon_client, alice):
        """После логина редирект на ?next=... если задан."""
        protected_url = reverse("users:user_list")
        login_url = f"{reverse('login')}?next={protected_url}"
        anon_client.post(login_url, {
            "username": alice.username,
            "password": "TestPass123!",
        })
        response = anon_client.get(protected_url)
        assert response.status_code == 200

    def test_login_wrong_password(self, anon_client, alice, urls):
        """Неправильный пароль — остаёмся на странице логина."""
        response = anon_client.post(urls["login"], {
            "username": alice.username,
            "password": "WrongPassword!",
        })
        assert response.status_code == 200

    def test_login_nonexistent_user(self, anon_client, urls):
        """Несуществующий пользователь — ошибка."""
        response = anon_client.post(urls["login"], {
            "username": "nobody",
            "password": "AnyPass123!",
        })
        assert response.status_code == 200

    def test_logout_success(self, auth_client, urls):
        """POST /auth/logout/ разлогинивает пользователя."""
        response = auth_client.post(urls["logout"])
        assert response.status_code == 302

    def test_logout_then_protected_redirects(self, auth_client, urls):
        """После выхода защищённые URL недоступны."""
        auth_client.post(urls["logout"])
        response = auth_client.get(urls["user_list"])
        assert response.status_code == 302
        assert "/login" in response["Location"]

    @pytest.mark.parametrize("username,password", [
        ("", "TestPass123!"),
        ("alice", ""),
        ("", ""),
        ("alice", "WRONGpass999!"),
        ("ALICE", "TestPass123!"),
    ])
    def test_login_invalid_credentials(self, anon_client, alice, urls, username, password):
        """Любые невалидные комбинации логина/пароля — статус 200 (не пускает)."""
        response = anon_client.post(urls["login"], {
            "username": username,
            "password": password,
        })
        assert response.status_code == 200


# 3. ПРАВА ДОСТУПА (АВТОРИЗАЦИЯ)

@pytest.mark.django_db
class TestAccessControl:
    """Кто что может делать — тесты разграничения доступа."""

    @pytest.mark.parametrize("url_name,kwargs", [
        ("users:user_list",    {}),
        ("users:profile_edit", {}),
    ])
    def test_anon_redirected_from_protected(self, anon_client, url_name, kwargs):
        """Анонимный пользователь перенаправляется с защищённых URL на логин."""
        url = reverse(url_name, kwargs=kwargs)
        response = anon_client.get(url)
        assert response.status_code == 302
        assert "/login" in response["Location"]

    def test_anon_redirected_from_profile(self, anon_client, alice):
        """Анонимный пользователь не может просматривать профиль."""
        url = reverse("users:profile", kwargs={"username": alice.username})
        response = anon_client.get(url)
        assert response.status_code == 302
        assert "/login" in response["Location"]

    def test_anon_can_access_register(self, anon_client, urls):
        """Анонимный пользователь может открыть страницу регистрации."""
        response = anon_client.get(urls["register"])
        assert response.status_code == 200

    def test_anon_can_access_login(self, anon_client, urls):
        """Анонимный пользователь может открыть страницу входа."""
        response = anon_client.get(urls["login"])
        assert response.status_code == 200

    def test_auth_can_see_own_profile(self, auth_client, alice):
        """Авторизованный пользователь видит свой профиль."""
        url = reverse("users:profile", kwargs={"username": alice.username})
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.context["is_own"] is True

    def test_auth_can_see_friend_profile(self, auth_client, alice, bob):
        """Авторизованный пользователь видит профиль друга."""
        alice.friends.add(bob)
        url = reverse("users:profile", kwargs={"username": bob.username})
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_auth_cannot_see_stranger_profile(self, auth_client, charlie):
        """Авторизованный пользователь НЕ может смотреть профиль незнакомца."""
        url = reverse("users:profile", kwargs={"username": charlie.username})
        response = auth_client.get(url)
        assert response.status_code == 302
        assert reverse("users:user_list") in response["Location"]

    def test_auth_cannot_see_stranger_profile_message(self, auth_client, charlie):
        """При попытке открыть чужой профиль показывается сообщение об ошибке."""
        url = reverse("users:profile", kwargs={"username": charlie.username})
        response = auth_client.get(url, follow=True)
        msgs = [str(m) for m in get_messages(response.wsgi_request)]
        assert any("друзей" in m for m in msgs)

    def test_auth_can_access_user_list(self, auth_client, urls):
        """Авторизованный пользователь видит список пользователей."""
        response = auth_client.get(urls["user_list"])
        assert response.status_code == 200

    def test_auth_can_edit_own_profile(self, auth_client, urls):
        """Авторизованный пользователь может открыть форму редактирования."""
        response = auth_client.get(urls["profile_edit"])
        assert response.status_code == 200
        assert isinstance(response.context["form"], ProfileEditForm)


# 4. РЕДИРЕКТЫ

@pytest.mark.django_db
class TestRedirects:
    """Тесты редиректов с assertRedirects."""

    def test_register_redirects_to_profile(self, anon_client, user_data, urls):
        """После регистрации — редирект на страницу профиля."""
        response = anon_client.post(urls["register"], data=user_data)
        expected = reverse("users:profile", kwargs={"username": user_data["username"]})
        assert response.status_code == 302
        assert response["Location"] == expected

    def test_login_redirects_to_home(self, anon_client, alice, urls):
        """После логина — редирект на LOGIN_REDIRECT_URL (/)."""
        response = anon_client.post(urls["login"], {
            "username": alice.username,
            "password": "TestPass123!",
        })
        assert response.status_code == 302

    def test_logout_redirects_to_home(self, auth_client, urls):
        """После выхода — редирект на LOGOUT_REDIRECT_URL (/)."""
        response = auth_client.post(urls["logout"])
        assert response.status_code == 302
        assert response["Location"] == "/"

    def test_anon_to_login_with_next(self, anon_client, alice):
        """Анонимный запрос к профилю — логин c ?next=..."""
        profile_url = reverse("users:profile", kwargs={"username": alice.username})
        response = anon_client.get(profile_url)
        assert response.status_code == 302
        assert "login" in response["Location"]
        assert "next" in response["Location"]

    def test_profile_edit_save_redirects(self, auth_client, alice, urls):
        """Сохранение профиля — редирект на страницу профиля."""
        data = {
            "first_name": "Алиса",
            "last_name": "Новая",
            "email": alice.email,
            "phone": "",
            "bio": "",
        }
        response = auth_client.post(urls["profile_edit"], data=data)
        expected = reverse("users:profile", kwargs={"username": alice.username})
        assert response.status_code == 302
        assert response["Location"] == expected

    def test_stranger_profile_redirects_to_user_list(self, auth_client, charlie):
        """Попытка открыть профиль незнакомца — редирект на user_list."""
        url = reverse("users:profile", kwargs={"username": charlie.username})
        response = auth_client.get(url)
        assert response.status_code == 302
        assert response["Location"] == reverse("users:user_list")

    def test_authenticated_register_redirects_to_own_profile(self, auth_client, alice, urls):
        """Залогиненный пользователь при GET /register — редирект на свой профиль."""
        response = auth_client.get(urls["register"])
        expected = reverse("users:profile", kwargs={"username": alice.username})
        assert response.status_code == 302
        assert response["Location"] == expected

    @pytest.mark.parametrize("url_name", [
        "users:user_list",
        "users:profile_edit",
    ])
    def test_anon_redirects_include_next_param(self, anon_client, url_name):
        """При редиректе анонима на логин URL содержит параметр next."""
        url = reverse(url_name)
        response = anon_client.get(url)
        assert response.status_code == 302
        assert "next=" in response["Location"]


# 5. СИСТЕМА ДРУЗЕЙ

@pytest.mark.django_db
class TestFriendSystem:
    """Тесты функциональности добавления / удаления друзей."""

    def test_send_friend_request(self, auth_client, alice, bob):
        """alice может отправить заявку bob."""
        url = reverse("users:send_friend_request", kwargs={"username": bob.username})
        auth_client.get(url)
        alice.refresh_from_db()
        assert alice.has_sent_request(bob)

    def test_cannot_send_request_to_self(self, auth_client, alice):
        """Нельзя отправить заявку самому себе."""
        url = reverse("users:send_friend_request", kwargs={"username": alice.username})
        auth_client.get(url, follow=True)
        alice.refresh_from_db()
        assert not alice.has_sent_request(alice)

    def test_accept_friend_request(self, bob_client, alice, bob):
        """bob принимает заявку от alice — оба становятся друзьями."""
        alice.friend_requests.add(bob)
        url = reverse("users:accept_friend_request", kwargs={"username": alice.username})
        bob_client.get(url)
        bob.refresh_from_db()
        alice.refresh_from_db()
        assert bob.is_friend(alice)
        assert alice.is_friend(bob)

    def test_accept_removes_request(self, bob_client, alice, bob):
        """После принятия заявка удаляется из pending_requests."""
        alice.friend_requests.add(bob)
        url = reverse("users:accept_friend_request", kwargs={"username": alice.username})
        bob_client.get(url)
        alice.refresh_from_db()
        assert not alice.has_sent_request(bob)

    def test_reject_friend_request(self, bob_client, alice, bob):
        """bob отклоняет заявку alice — не становятся друзьями."""
        alice.friend_requests.add(bob)
        url = reverse("users:reject_friend_request", kwargs={"username": alice.username})
        bob_client.get(url)
        bob.refresh_from_db()
        assert not bob.is_friend(alice)
        assert not alice.has_sent_request(bob)

    def test_remove_friend(self, auth_client, alice_and_bob_friends):
        """alice удаляет bob из друзей."""
        alice, bob = alice_and_bob_friends
        url = reverse("users:remove_friend", kwargs={"username": bob.username})
        auth_client.get(url)
        alice.refresh_from_db()
        assert not alice.is_friend(bob)

    def test_remove_friend_is_symmetric(self, auth_client, alice_and_bob_friends):
        """После удаления bob тоже теряет alice из друзей."""
        alice, bob = alice_and_bob_friends
        url = reverse("users:remove_friend", kwargs={"username": bob.username})
        auth_client.get(url)
        bob.refresh_from_db()
        assert not bob.is_friend(alice)

    def test_duplicate_friend_request_ignored(self, auth_client, alice, bob):
        """Повторная заявка игнорируется."""
        alice.friend_requests.add(bob)
        url = reverse("users:send_friend_request", kwargs={"username": bob.username})
        auth_client.get(url, follow=True)
        assert alice.friend_requests.filter(pk=bob.pk).count() == 1

    def test_friends_profile_visible(self, auth_client, alice, bob):
        """alice видит профиль bob, если они друзья."""
        alice.friends.add(bob)
        url = reverse("users:profile", kwargs={"username": bob.username})
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.context["is_friend"] is True

    def test_user_list_shows_friend_status(self, auth_client, alice, bob):
        """На странице списка bob виден среди друзей alice."""
        alice.friends.add(bob)
        url = reverse("users:user_list")
        response = auth_client.get(url)
        assert response.status_code == 200
        assert bob in response.context["friends"]


# 6. МОДЕЛЬ И ФОРМЫ

@pytest.mark.django_db
class TestUserModel:
    """Тесты модели CustomUser."""

    def test_str_returns_username(self, alice):
        """__str__ возвращает username."""
        assert str(alice) == alice.username

    def test_email_unique(self, create_user):
        """Нельзя создать двух пользователей с одним email."""
        from django.db import IntegrityError
        create_user(username="u1", email="same@test.com")
        with pytest.raises(IntegrityError):
            create_user(username="u2", email="same@test.com")

    def test_default_role_is_student(self, create_user):
        """Роль по умолчанию — student."""
        user = create_user(username="newuser")
        assert user.role == "student"

    @pytest.mark.parametrize("role", ["student", "teacher", "admin"])
    def test_valid_roles(self, create_user, role):
        """Все допустимые роли принимаются без ошибок."""
        user = create_user(username=f"user_{role}", email=f"{role}@test.com", role=role)
        assert user.role == role

    def test_is_friend_false_by_default(self, alice, bob):
        """is_friend возвращает False для незнакомых."""
        assert not alice.is_friend(bob)

    def test_has_sent_request_false_by_default(self, alice, bob):
        """has_sent_request возвращает False до отправки заявки."""
        assert not alice.has_sent_request(bob)

    def test_friends_symmetrical(self, alice, bob):
        """Добавление в друзья симметрично."""
        alice.friends.add(bob)
        assert alice.is_friend(bob)
        assert bob.is_friend(alice)


@pytest.mark.django_db
class TestRegistrationForm:
    """Тесты формы регистрации."""

    def test_valid_form(self, user_data):
        """Валидные данные — форма валидна."""
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid(), form.errors

    def test_duplicate_email_in_form(self, alice, user_data):
        """Форма с уже существующим email невалидна."""
        user_data["email"] = alice.email
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
        assert "email" in form.errors

    @pytest.mark.parametrize("field", ["username", "first_name", "last_name", "email"])
    def test_required_fields_in_form(self, user_data, field):
        """Обязательные поля не могут быть пустыми."""
        user_data[field] = ""
        form = CustomUserCreationForm(data=user_data)
        assert not form.is_valid()
        assert field in form.errors

    def test_phone_optional(self, user_data):
        """Телефон необязателен."""
        user_data["phone"] = ""
        form = CustomUserCreationForm(data=user_data)
        assert form.is_valid(), form.errors


# 7. ОШИБКИ (404, невалидные запросы)

@pytest.mark.django_db
class TestErrors:
    """Тесты обработки ошибок."""

    def test_profile_404_for_nonexistent_user(self, auth_client):
        """Профиль несуществующего пользователя — 404."""
        url = reverse("users:profile", kwargs={"username": "does_not_exist"})
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_send_request_404_for_nonexistent_user(self, auth_client):
        """Заявка несуществующему пользователю — 404."""
        url = reverse("users:send_friend_request", kwargs={"username": "ghost"})
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_accept_request_404_for_nonexistent_user(self, auth_client):
        """Принятие заявки от несуществующего пользователя — 404."""
        url = reverse("users:accept_friend_request", kwargs={"username": "ghost"})
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_remove_friend_404_for_nonexistent_user(self, auth_client):
        """Удаление несуществующего пользователя из друзей — 404."""
        url = reverse("users:remove_friend", kwargs={"username": "ghost"})
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_profile_edit_invalid_email(self, auth_client, alice, urls):
        """Невалидный email при редактировании профиля — форма с ошибкой."""
        response = auth_client.post(urls["profile_edit"], data={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "not-an-email",
            "phone": "",
            "bio": "",
        })
        assert response.status_code == 200
        assert "email" in response.context["form"].errors

    def test_profile_edit_duplicate_email(self, auth_client, alice, bob, urls):
        """При редактировании нельзя установить email другого пользователя."""
        response = auth_client.post(urls["profile_edit"], data={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": bob.email,
            "phone": "",
            "bio": "",
        })
        assert response.status_code == 200
        assert "email" in response.context["form"].errors

    @pytest.mark.parametrize("bad_username", [
        "nonexistent_user_xyz",
        "123456789",
        "no_such_person",
    ])
    def test_profile_nonexistent_users(self, auth_client, bad_username):
        """GET профиля с несуществующим username — 404."""
        url = reverse("users:profile", kwargs={"username": bad_username})
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_accept_nonexistent_request_shows_error(self, auth_client, bob):
        """Принятие заявки, которой нет, показывает сообщение об ошибке."""
        url = reverse("users:accept_friend_request", kwargs={"username": bob.username})
        response = auth_client.get(url, follow=True)
        msgs = [str(m) for m in get_messages(response.wsgi_request)]
        assert any("не найдена" in m or "Заявка" in m for m in msgs)
