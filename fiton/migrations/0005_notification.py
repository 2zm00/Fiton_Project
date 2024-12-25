# Generated by Django 5.1.3 on 2024-12-25 14:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiton', '0004_alter_instructor_average_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='알림 메시지')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('is_read', models.BooleanField(default=False, verbose_name='읽음 여부')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
    ]
