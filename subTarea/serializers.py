from rest_framework import serializers
from core.models import TareaSubordinada


### SERIALIZADOR ###
class SubTareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = TareaSubordinada
        fields = ('id','titulo_tarea_sub','descripcion_tarea_sub')
        read_only_Fields = ('id',)
