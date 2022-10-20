from rest_framework import serializers
from core.models import Rol


### SERIALIZADOR PARA EL ROL ###
class RolSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Rol
        fields = ('id','rol_name','unidad_id')
        read_only_Fields = ('id',)
