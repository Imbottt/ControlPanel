# Generated by Django 4.1.1 on 2022-10-15 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_user_rol_remove_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.DeleteModel(
            name='Roll',
        ),
    ]