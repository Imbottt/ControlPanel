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
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()

    # Validaciones
    def validate(self, data):
        if data['fecha_fin'] < data['fecha_inicio']:
            raise serializers.ValidationError("La fecha de fin no puede ser menor a la fecha de inicio")
        elif data['fecha_fin'] == "":
            raise serializers.ValidationError("El campo fecha fin no puede estar vacío")
        elif data['fecha_inicio'] == "":
            raise serializers.ValidationError("El campo fecha de inicio no puede estar vacío")
        return data

    class Meta:
        model = Flujo
        fields = ['id','flujo_name','descripcion_flujo','fecha_creacion','fecha_actualizacion','fecha_inicio','fecha_fin','plazo_flujo','creador_flujo','ejecutar']
        read_only_Fields = ('id',)

    def create(self, validated_data):
        return Flujo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        fecha_ini = validated_data.pop('fecha_inicio')
        fecha_fin = validated_data.pop('fecha_fin')
        flujo = super().update(instance, validated_data)

        if fecha_ini and fecha_fin:
            flujo = Flujo.objects.get(fecha_ini = self.fecha_inicio)
            flujo = Flujo.objects.get(fecha_fin = self.fecha_fin)
            flujo.save()
            flujo.append(Flujo.objects.create(**flujo))
            instance.flujo.add(*flujo)
            return instance
    
