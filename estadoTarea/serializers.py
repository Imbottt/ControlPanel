from rest_framework import serializers
from core.models import EstadoTarea


### SERIALIZADOR ###
class EstadoTareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Estado-Tarea """
    class Meta:
        model = EstadoTarea
        fields = ('id','estado_name','descripcion_estado')
        read_only_Fields = ('id',)