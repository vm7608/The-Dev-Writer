# Generated by Django 4.2 on 2023-05-16 15:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0004_savepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='savepost',
            name='date_saved',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]