# Generated by Django 5.1.3 on 2024-12-28 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiton', '0003_center_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='exercises',
            field=models.ManyToManyField(blank=True, to='fiton.exercise', verbose_name='운동 종목'),
        ),
    ]