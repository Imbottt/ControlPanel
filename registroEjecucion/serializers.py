from rest_framework import serializers
from core.models import RegistroEjecucion


### SERIALIZADOR ###
class RegistroExeSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = RegistroEjecucion
        fields = ('id','confirmacion','justificacion','observacion','fecha_registro')
        read_only_Fields = ('id',)

### SERIALIZADOR PARA LISTAR EL REGISTRO DE EJECUCIÓN DE LAS TAREAS ###
class RegistroExeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroEjecucion

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'confirmacion': instance['rol_name'],
            'justificacion': instance['rol_name'],
            'observacion': instance['rol_name'],
            'fecha_registro': instance['rol_name'],
        }

### SERIALIZADOR PARA ACTUALIZAR LA EJECUCIÓN DE LAS TAREAS ###
class UpdateRegistroExeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroEjecucion
        fields = ('id','confirmacion','justificacion','observacion','fecha_registro')