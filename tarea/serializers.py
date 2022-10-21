from rest_framework import serializers
from core.models import Tarea


### SERIALIZADOR ###
class TareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Tarea """
    class Meta:
        model = Tarea
        fields = ('id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_limite','progreso_tarea','detalle_flujo_id')
        read_only_Fields = ('id',)

