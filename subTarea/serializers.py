from rest_framework import serializers
from core.models import TareaSubordinada


### SERIALIZADOR ###
class SubTareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = TareaSubordinada
        fields = ('id','titulo_subTarea','descripcion_subTarea','fecha_creacion','fecha_inicio','fecha_fin','tarea')
        read_only_Fields = ('id',)
 