# Generated by Django 4.1.1 on 2022-10-12 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_last_name_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rol',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]