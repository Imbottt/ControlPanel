from rest_framework import serializers
from core.models import Flujo

###
from datetime import datetime

### SERIALIZADOR PARA EL FLUJO ###
class FlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Flujo """
    descripcion_flujo = serializers.CharField(allow_null=False, allow_blank=False)
    fecha_creacion = serializers.DateField(read_only=True)
    fecha_actualizacion = serializers.DateField(read_only=True)
    plazo_flujo = serializers.CharField(read_only=True)
    class Meta:
        model = Flujo
        fields = ['id','flujo_name','descripcion_flujo','fecha_creacion','fecha_actualizacion','fecha_inicio','fecha_fin','plazo_flujo','creador_flujo','ejecutar']
        read_only_Fields = ('id',)
    
