from rest_framework import serializers
from core.models import Unidad


### SERIALIZADOR ###
class UnidadSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Unidad
        fields = ('id','unidad_name')
        read_only_Fields = ('id',)

### SERIALIZADOR PARA LISTAR LOS ROLES ###
class UnidadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'unidad_name': instance['unidad_name'],
        }

### SERIALIZADOR PARA ACTUALIZAR LOS ROLES ###
class UpdateUnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = ('id','unidad_name')