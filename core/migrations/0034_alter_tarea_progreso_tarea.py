# Generated by Django 4.1.1 on 2022-10-28 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_tarea_progreso_tarea'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='progreso_tarea',
            field=models.FloatField(),
        ),
    ]