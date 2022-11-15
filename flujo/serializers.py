from rest_framework import serializers
from core.models import Flujo

### SERIALIZADOR PARA EL FLUJO ###
class FlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Flujo """
    plazo_flujo = serializers.CharField(read_only=True)
    progreso_f = serializers.CharField(read_only=True)
    class Meta:
        model = Flujo
        fields = ['id','flujo_name','descripcion_flujo','fecha_creacion','fecha_inicio','fecha_fin','plazo_flujo','progreso_f','is_active']
        read_only_Fields = ('id','fecha_creacion',)
    
    def create(self, validated_data):
        """ Crear nuevo usuario con clave encriptada y retornarlo """
        return Flujo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """ Actualiza el flujo """
        instance.fecha_inicio = validated_data.get('fecha_inicio', None)
        instance.fecha_fin = validated_data.get('fecha_fin', None)
        instance.save()
        return instance
        

### SERIALIZADOR PARA ACTUALIZAR EL FLUJO ###
class UpdateFlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el actualizador del flujo """
    plazo_flujo = serializers.CharField(read_only=True)
    class Meta:
        model = Flujo
        fields = ['id','flujo_name','descripcion_flujo','fecha_inicio','fecha_fin','plazo_flujo','progreso_f','is_active']
        read_only_Fields = ('id','fecha_creacion',)