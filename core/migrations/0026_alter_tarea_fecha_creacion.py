# Generated by Django 4.1.1 on 2022-10-27 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_tarea_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='fecha_creacion',
            field=models.DateField(null=True),
        ),
    ]
