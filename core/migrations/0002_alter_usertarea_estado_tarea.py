# Generated by Django 4.1.1 on 2022-11-27 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertarea',
            name='estado_tarea',
            field=models.CharField(choices=[('0', 'Sin asignar'), ('1', 'Por empezar'), ('2', 'En progreso'), ('3', 'Finalizada')], default=None, max_length=12),
        ),
    ]
