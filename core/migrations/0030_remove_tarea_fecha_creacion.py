# Generated by Django 4.1.1 on 2022-10-27 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_tarea_fecha_inicio_tarea_fecha_limite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarea',
            name='fecha_creacion',
        ),
    ]