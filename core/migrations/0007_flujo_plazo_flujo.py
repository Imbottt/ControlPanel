# Generated by Django 4.1.1 on 2022-11-09 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_direccion_fecha_hoy_tarea_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flujo',
            name='plazo_flujo',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
