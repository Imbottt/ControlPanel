# Generated by Django 4.1.1 on 2022-10-25 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_rename_alerta_alertas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertas',
            name='alerta_name',
        ),
        migrations.AlterField(
            model_name='alertas',
            name='confirmacion',
            field=models.CharField(choices=[('0', '--------'), ('1', 'Aceptado'), ('2', 'Rechazado')], default=0, max_length=10),
        ),
    ]
