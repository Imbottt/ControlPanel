from rest_framework import serializers
from core.models import TareaSubordinada


### SERIALIZADOR ###
class SubTareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = TareaSubordinada
        fields = ('id','titulo_tarea_sub','descripcion_tarea_sub')
        read_only_Fields = ('id',)

### SERIALIZADOR PARA LISTAR LOS ROLES ###
class SubTareaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaSubordinada

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'titulo_tarea_sub': instance['titulo_tarea_sub'],
            'descripcion_tarea_sub': instance['descripcion_tarea_sub'],
        }

### SERIALIZADOR PARA ACTUALIZAR LOS ROLES ###
class UpdateSubTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaSubordinada
        fields = ('id','titulo_tarea_sub','descripcion_tarea_sub')