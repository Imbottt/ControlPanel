from rest_framework import serializers
from core.models import Rol


### SERIALIZADOR ###
class RolSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Rol
        fields = ('id','rol_name')
        read_only_Fields = ('id',)

### SERIALIZADOR PARA LISTAR LOS ROLES ###
class RolListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'rol_name': instance['rol_name'],
        }

### SERIALIZADOR PARA ACTUALIZAR LOS ROLES ###
class UpdateRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ('id','rol_name')