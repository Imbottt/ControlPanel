# Generated by Django 4.1.1 on 2022-12-03 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_notificacion_id_tarea_notificacion_tarea'),
    ]

    operations = [
        migrations.CreateModel(
            name='TareaRelacionada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_tarea_main', models.PositiveIntegerField(null=True)),
                ('id_tarea_relational', models.PositiveIntegerField(null=True)),
            ],
        ),
    ]