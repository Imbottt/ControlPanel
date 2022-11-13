from rest_framework import serializers
from core.models import Flujo

### SERIALIZADOR PARA EL FLUJO ###
class FlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Flujo """
    plazo_flujo = serializers.CharField(read_only=True)
    class Meta:
        model = Flujo
        fields = ['id','flujo_name','descripcion_flujo','fecha_creacion','fecha_inicio','fecha_fin','plazo_flujo']
        read_only_Fields = ('id','fecha_creacion',)

### SERIALIZADOR PARA ACTUALIZAR EL FLUJO ###
class UpdateFlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el actualizador del flujo """
    plazo_flujo = serializers.CharField(read_only=True)
    class Meta:
        model = Flujo
        fields = ['id','flujo_name','descripcion_flujo','fecha_inicio','fecha_fin','plazo_flujo']
        read_only_Fields = ('id','fecha_creacion',)