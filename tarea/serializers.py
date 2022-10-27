from rest_framework import serializers
from core.models import Tarea, EstadoTarea

### SERIALIZADOR ESTADO TAREA###
class EstadoTareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Estado-Tarea """
    class Meta:
        model = EstadoTarea
        fields = ['estado_name']

### SERIALIZADOR ###
class TareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Tarea """
    class Meta:
        model = Tarea
        fields = ('id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_inicio','fecha_limite','progreso_tarea','estado')
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['estado'] = EstadoTareaSerializer(instance.estado).data
        return response

    def get_total(self, obj):
        return obj.Tarea.aggregate(Total=(sum('fecha_limite')) - sum('fecha_inicio'))

    def save(self, *args, **kwargs):
        self.total_descuento = self.get_total_descuento
        self.progreso_tarea = self.get_total
        super(Tarea, self).save(*args, **kwargs)