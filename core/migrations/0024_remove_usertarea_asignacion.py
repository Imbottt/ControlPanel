# Generated by Django 4.1.1 on 2022-10-27 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_user_creador'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertarea',
            name='asignacion',
        ),
    ]
