# Generated by Django 4.1.1 on 2022-10-26 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_tarea_hora_inicio_tarea_hora_limite_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarea',
            name='hora_inicio',
        ),
        migrations.RemoveField(
            model_name='tarea',
            name='hora_limite',
        ),
    ]