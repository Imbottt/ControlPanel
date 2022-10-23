from rest_framework import serializers
from core.models import Rol, Unidad


### SERIALIZADOR PARA LA UNIDAD ###
class UnidadSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Unidad
        fields = '__all__' #('id','unidad_name')
        read_only_Fields = ('id',)

### SERIALIZADOR PARA EL ROL ###
class RolSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Rol
        fields =  '__all__' #('id','rol_name','unidad_id')
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['unidad_id'] = UnidadSerializer(instance.unidad_id).data
        return response
