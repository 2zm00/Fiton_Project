# Generated by Django 5.1.3 on 2024-12-16 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiton', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
