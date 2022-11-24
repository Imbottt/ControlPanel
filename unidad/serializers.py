from rest_framework import serializers
from core.models import Unidad, Direccion

### SERIALIZADOR DE DIRECCIÓN ###
class DirSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Dirección """
    dir_name = serializers.CharField(allow_null=False, required=True, allow_blank=False, min_length=4)

    class Meta:
        model = Direccion
        fields = ['id','dir_name']
        read_only_Fields = ('id',)

### SERIALIZADOR DE UNIDAD ###
class UnidadSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Unidad """
    unidad_name = serializers.CharField(allow_null=False, required=True, allow_blank=False, min_length=3)

    class Meta:
        model = Unidad
        fields = ('id','unidad_name','dir')
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['dir'] = DirSerializer(instance.dir).data
        return response
