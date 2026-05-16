import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomUserCreationForm, ProfileEditForm
from .models import CustomUser


# логер уровня модуля
logger = logging.getLogger(__name__)  # 'users.views'


# РЕГИСТРАЦИЯ

def register(request):
    """Регистрация нового пользователя."""
    if request.user.is_authenticated:
        logger.debug(
            "Authenticated user '%s' tried to open register page — redirecting.",
            request.user.username,
        )
        return redirect('users:profile', username=request.user.username)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # успешная регистрация → INFO
            logger.info(
                "New user registered and logged in: username='%s', email='%s', role='%s'",
                user.username,
                user.email,
                user.role,
            )

            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('users:profile', username=user.username)

        else:
            # ошибки валидации при регистрации → WARNING
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(
                        "Registration validation error: field='%s', error='%s', "
                        "attempted_username='%s'",
                        field,
                        error,
                        request.POST.get('username', '<unknown>'),
                    )
                    messages.error(request, error)

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# ПРОФИЛЬ

@login_required
def profile(request, username):
    """Страница профиля пользователя."""
    profile_user = get_object_or_404(CustomUser, username=username)
    is_own = request.user == profile_user
    is_friend = request.user.is_friend(profile_user)
    has_sent = request.user.has_sent_request(profile_user)
    has_incoming = profile_user.has_sent_request(request.user)

    if not is_own and not is_friend:
        logger.warning(
            "Access denied: user='%s' tried to view profile of stranger='%s'",
            request.user.username,
            username,
        )
        messages.error(request, 'Вы можете просматривать только страницы своих друзей.')
        return redirect('users:user_list')

    logger.debug(
        "Profile viewed: viewer='%s', profile='%s', is_own=%s, is_friend=%s",
        request.user.username,
        username,
        is_own,
        is_friend,
    )

    context = {
        'profile_user': profile_user,
        'is_own': is_own,
        'is_friend': is_friend,
        'has_sent': has_sent,
        'has_incoming': has_incoming,
    }
    return render(request, 'users/profile.html', context)


# РЕДАКТИРОВАНИЕ ПРОФИЛЯ (с логированием ошибки загрузки файла)

@login_required
def profile_edit(request):
    """Редактирование своего профиля."""
    if request.method == 'POST':

        # Логирование ошибки загрузки не-изображения (exc_info=True)
        avatar_file = request.FILES.get('avatar')
        if avatar_file:
            _validate_avatar(avatar_file, request.user.username)

        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            logger.info(
                "Profile updated: user='%s'",
                request.user.username,
            )
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('users:profile', username=request.user.username)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(
                        "Profile edit validation error: user='%s', field='%s', error='%s'",
                        request.user.username,
                        field,
                        error,
                    )
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'users/profile_edit.html', {'form': form})


def _validate_avatar(file, username: str) -> None:
    """
    Проверяет, что загруженный файл является изображением.
    Логирует ошибку с exc_info=True, но НЕ глушит исключение полностью —
    невалидный файл просто не пройдёт форму (ImageField сам отклонит).
    """
    try:
        from PIL import Image
        img = Image.open(file)
        img.verify()          # бросит исключение, если это не изображение
        file.seek(0)          # сбрасываем указатель после verify()
        logger.debug(
            "Avatar file passed PIL verification: user='%s', filename='%s', format='%s'",
            username,
            file.name,
            img.format,
        )
    except Exception:
        # exc_info=True — в лог попадёт полный traceback
        # Ошибку не глушим: форма (ImageField) сама выдаст ошибку пользователю
        logger.warning(
            "Invalid avatar file uploaded: user='%s', filename='%s', "
            "content_type='%s' — not a valid image",
            username,
            file.name,
            getattr(file, 'content_type', 'unknown'),
            exc_info=True,
        )
        file.seek(0)  # сбрасываем указатель, чтобы форма могла прочитать файл


# СПИСОК ПОЛЬЗОВАТЕЛЕЙ

@login_required
def user_list(request):
    """Список всех пользователей."""
    users = CustomUser.objects.exclude(pk=request.user.pk).order_by('username')
    friends = request.user.friends.all()
    incoming = request.user.pending_requests.all()
    outgoing = request.user.friend_requests.all()

    logger.debug(
        "User list accessed: user='%s', total_users=%d, friends=%d",
        request.user.username,
        users.count(),
        friends.count(),
    )

    context = {
        'users': users,
        'friends': friends,
        'incoming': incoming,
        'outgoing': outgoing,
    }
    return render(request, 'users/user_list.html', context)


# СИСТЕМА ДРУЗЕЙ

@login_required
def send_friend_request(request, username):
    """Отправить заявку в друзья."""
    to_user = get_object_or_404(CustomUser, username=username)

    if to_user == request.user:
        logger.warning(
            "Self friend-request attempt: user='%s'",
            request.user.username,
        )
        messages.error(request, 'Нельзя добавить себя в друзья.')

    elif request.user.is_friend(to_user):
        logger.debug(
            "Duplicate friend attempt (already friends): from='%s', to='%s'",
            request.user.username,
            to_user.username,
        )
        messages.info(request, f'{to_user.username} уже у вас в друзьях.')

    elif request.user.has_sent_request(to_user):
        logger.debug(
            "Duplicate friend request (already pending): from='%s', to='%s'",
            request.user.username,
            to_user.username,
        )
        messages.info(request, 'Заявка уже отправлена.')

    else:
        request.user.friend_requests.add(to_user)
        # отправка заявки → INFO
        logger.info(
            "Friend request sent: from='%s', to='%s'",
            request.user.username,
            to_user.username,
        )
        messages.success(request, f'Заявка пользователю {to_user.username} отправлена.')

    return redirect(request.META.get('HTTP_REFERER', 'users:user_list'))


@login_required
def accept_friend_request(request, username):
    """Принять заявку в друзья."""
    from_user = get_object_or_404(CustomUser, username=username)

    if from_user.has_sent_request(request.user):
        request.user.friends.add(from_user)
        from_user.friend_requests.remove(request.user)

        # принятие заявки → INFO
        logger.info(
            "Friend request accepted: user='%s' accepted request from='%s'",
            request.user.username,
            from_user.username,
        )
        messages.success(request, f'{from_user.username} теперь ваш друг!')
    else:
        logger.warning(
            "Accept failed — no pending request: user='%s', from='%s'",
            request.user.username,
            from_user.username,
        )
        messages.error(request, 'Заявка не найдена.')

    return redirect(request.META.get('HTTP_REFERER', 'users:user_list'))


@login_required
def reject_friend_request(request, username):
    """Отклонить заявку в друзья."""
    from_user = get_object_or_404(CustomUser, username=username)
    from_user.friend_requests.remove(request.user)

    logger.info(
        "Friend request rejected: user='%s' rejected request from='%s'",
        request.user.username,
        from_user.username,
    )
    messages.info(request, f'Заявка от {from_user.username} отклонена.')
    return redirect(request.META.get('HTTP_REFERER', 'users:user_list'))


@login_required
def remove_friend(request, username):
    """Удалить из друзей."""
    friend = get_object_or_404(CustomUser, username=username)
    request.user.friends.remove(friend)

    # удаление из друзей → INFO
    logger.info(
        "Friend removed: user='%s' removed friend='%s'",
        request.user.username,
        friend.username,
    )
    messages.info(request, f'{friend.username} удалён из друзей.')
    return redirect(request.META.get('HTTP_REFERER', 'users:user_list'))
