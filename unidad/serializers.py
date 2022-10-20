from rest_framework import serializers
from core.models import Unidad


### SERIALIZADOR ###
class UnidadSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Unidad
        fields = ('id','unidad_name')
        read_only_Fields = ('id',)