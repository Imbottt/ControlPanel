# Generated by Django 4.1.1 on 2022-10-27 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_tarea_hora_inicio_remove_tarea_hora_limite'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='creador',
            field=models.IntegerField(default=0),
        ),
    ]
