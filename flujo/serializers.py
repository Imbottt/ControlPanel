from rest_framework import serializers
from core.models import Flujo

### SERIALIZADOR PARA EL FLUJO ###
class FlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Flujo """
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()
    descripcion_flujo = serializers.CharField(allow_null=False, allow_blank=False)
    plazo_flujo = serializers.CharField(read_only=True)
    progreso_f = serializers.CharField(read_only=True)
    class Meta:
        model = Flujo
        fields = ['id','flujo_name','descripcion_flujo','fecha_creacion','fecha_inicio','fecha_fin','plazo_flujo','progreso_f','creador_flujo','ejecutar']
        read_only_Fields = ('id','fecha_creacion',)
    
    def create(self, validated_data):
        """ Crear nuevo usuario con clave encriptada y retornarlo """
        return Flujo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Actualizar datos de orden
        instance.flujo_name = validated_data.get('flujo_name', instance.flujo_name)
        instance.descripcion_flujo = validated_data.get('descripcion_flujo', instance.descripcion_flujo)
        instance.fecha_inicio = validated_data.get('fecha_inicio', instance.fecha_inicio)
        instance.fecha_fin = validated_data.get('fecha_fin', instance.fecha_fin)
        instance.ejecutar = validated_data.get('ejecutar', instance.ejecutar)
        instance.save()
        return instance

### SERIALIZADOR PARA ACTUALIZAR EL FLUJO ###
class UpdateFlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el actualizador del flujo """
    plazo_flujo = serializers.CharField(read_only=True)
    class Meta:
        model = Flujo
        fields = ['id','flujo_name','descripcion_flujo','fecha_inicio','fecha_fin','plazo_flujo','progreso_f','creador_flujo','ejecutar']
        read_only_Fields = ('id','fecha_creacion',)