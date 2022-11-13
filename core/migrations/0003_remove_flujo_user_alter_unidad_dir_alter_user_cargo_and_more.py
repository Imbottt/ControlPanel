# Generated by Django 4.1.1 on 2022-11-04 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_usertarea_estado_tarea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flujo',
            name='user',
        ),
        migrations.AlterField(
            model_name='unidad',
            name='dir',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.direccion'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cargo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.cargo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='rol',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.rol'),
        ),
        migrations.AlterField(
            model_name='user',
            name='unidad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.unidad'),
        ),
        migrations.AlterField(
            model_name='usertarea',
            name='estado_tarea',
            field=models.CharField(choices=[('Sin asignar', '1'), ('En progreso', '2'), ('Finalizada', '3')], default=None, max_length=12),
        ),
    ]
