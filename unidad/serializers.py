from rest_framework import serializers
from core.models import Unidad, Direccion

### SERIALIZADOR DE DIRECCIÓN ###
class DirSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Dirección """
    class Meta:
        model = Direccion
        fields = ['dir_name']

### SERIALIZADOR DE UNIDAD ###
class UnidadSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Unidad
        fields = ('id','unidad_name','dir')
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['dir'] = DirSerializer(instance.dir).data
        return response