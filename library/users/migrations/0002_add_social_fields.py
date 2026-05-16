import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        # Сделать email уникальным
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        # Добавить поле bio
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, verbose_name='О себе'),
        ),
        # M2M «друзья» (симметричное)
        migrations.AddField(
            model_name='customuser',
            name='friends',
            field=models.ManyToManyField(
                blank=True,
                related_name='friends_rel',
                symmetrical=True,
                to=settings.AUTH_USER_MODEL,
                verbose_name='Друзья',
            ),
        ),
        # M2M «заявки в друзья» (несимметричное)
        migrations.AddField(
            model_name='customuser',
            name='friend_requests',
            field=models.ManyToManyField(
                blank=True,
                related_name='pending_requests',
                symmetrical=False,
                to=settings.AUTH_USER_MODEL,
                verbose_name='Заявки в друзья',
            ),
        ),
    ]
