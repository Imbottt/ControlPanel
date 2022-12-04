from rest_framework import serializers
from core.models import TareaSubordinada, Tarea

### SERIALIZADOR ###
class TareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Tarea """
    plazo_tarea = serializers.CharField(read_only=True)
    progreso_tarea = serializers.CharField(read_only=True)
    class Meta:
        model = Tarea
        fields = ['id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_inicio','fecha_limite','plazo_tarea','progreso_tarea','creador_tarea']
        read_only_Fields = ('id')

### SERIALIZADOR ###
class SubTareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = TareaSubordinada
        fields = ('id','titulo_subTarea','descripcion_subTarea','fecha_creacion','fecha_inicio','fecha_fin','tarea')
        read_only_Fields = ('id',)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tarea'] = TareaSerializer(instance.tarea).data
        return response