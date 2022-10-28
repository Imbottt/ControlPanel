# Generated by Django 4.1.1 on 2022-10-25 23:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_rol_unidad_id_alter_user_cargo_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alerta_name', models.CharField(max_length=50, unique=True)),
                ('confirmacion', models.CharField(max_length=255)),
                ('justificacion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserTarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignacion', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='registroejecucion',
            old_name='fecha_registro',
            new_name='fecha_reg',
        ),
        migrations.RenameField(
            model_name='registroejecucion',
            old_name='titulo_registro',
            new_name='titulo_reg',
        ),
        migrations.RenameField(
            model_name='tareasubordinada',
            old_name='descripcion_tarea_sub',
            new_name='descripcion_subTarea',
        ),
        migrations.RenameField(
            model_name='tareasubordinada',
            old_name='titulo_tarea_sub',
            new_name='titulo_subTarea',
        ),
        migrations.RemoveField(
            model_name='flujo',
            name='titulo_flujo',
        ),
        migrations.RemoveField(
            model_name='registroejecucion',
            name='confirmacion',
        ),
        migrations.RemoveField(
            model_name='registroejecucion',
            name='estado_t_id',
        ),
        migrations.RemoveField(
            model_name='registroejecucion',
            name='justificacion',
        ),
        migrations.RemoveField(
            model_name='registroejecucion',
            name='observacion',
        ),
        migrations.RemoveField(
            model_name='registroejecucion',
            name='tarea_sub_id',
        ),
        migrations.RemoveField(
            model_name='registroejecucion',
            name='usuario_id',
        ),
        migrations.RemoveField(
            model_name='rol',
            name='unidad_id',
        ),
        migrations.RemoveField(
            model_name='tarea',
            name='detalle_flujo_id',
        ),
        migrations.RemoveField(
            model_name='tareasubordinada',
            name='tarea_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='cargo_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='dir_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rol_id',
        ),
        migrations.AddField(
            model_name='flujo',
            name='descripcion_flujo',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flujo',
            name='fecha_creacion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='flujo',
            name='fecha_fin',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='flujo',
            name='fecha_inicio',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='flujo',
            name='flujo_name',
            field=models.CharField(default=None, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flujo',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tarea',
            name='estado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.estadotarea'),
        ),
        migrations.AddField(
            model_name='tarea',
            name='fecha_inicio',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='tareasubordinada',
            name='fecha_creacion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='tareasubordinada',
            name='fecha_fin',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='tareasubordinada',
            name='fecha_inicio',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='tareasubordinada',
            name='tarea',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tarea'),
        ),
        migrations.AddField(
            model_name='unidad',
            name='dir',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.direccion'),
        ),
        migrations.AddField(
            model_name='user',
            name='cargo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.cargo'),
        ),
        migrations.AddField(
            model_name='user',
            name='rol',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.rol'),
        ),
        migrations.AddField(
            model_name='user',
            name='unidad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.unidad'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='cargo_name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='titulo_tarea',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.DeleteModel(
            name='DetalleFlujo',
        ),
        migrations.AddField(
            model_name='usertarea',
            name='tarea',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tarea'),
        ),
        migrations.AddField(
            model_name='usertarea',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='alerta',
            name='tarea',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tarea'),
        ),
        migrations.AddField(
            model_name='registroejecucion',
            name='userTarea',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.usertarea'),
        ),
    ]