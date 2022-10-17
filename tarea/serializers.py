from rest_framework import serializers
from core.models import Tarea


### SERIALIZADOR ###
class TareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Tarea
        fields = ('id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_limite','progreso_tarea')
        read_only_Fields = ('id',)

### SERIALIZADOR PARA LISTAR LOS ROLES ###
class TareaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'titulo_tarea': instance['titulo_tarea'],
            'descripcion_tarea': instance['descripcion_tarea'],
            'fecha_creacion': instance['fecha_creacion'],
            'fecha_limite': instance['fecha_limite'],
            'progreso_tarea': instance['progreso_tarea'],
        }

### SERIALIZADOR PARA ACTUALIZAR LOS ROLES ###
class UpdateTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ('id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_limite','progreso_tarea')