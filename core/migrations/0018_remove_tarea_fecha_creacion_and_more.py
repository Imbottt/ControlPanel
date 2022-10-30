# Generated by Django 4.1.1 on 2022-10-26 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_remove_alertas_alerta_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarea',
            name='fecha_creacion',
        ),
        migrations.AlterField(
            model_name='alertas',
            name='confirmacion',
            field=models.CharField(choices=[('0', '--------'), ('1', 'Acepto'), ('2', 'Rechazo')], default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='fecha_inicio',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='fecha_limite',
            field=models.DateTimeField(null=True),
        ),
    ]
