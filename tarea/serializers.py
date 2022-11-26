from rest_framework import serializers
from core.models import Tarea

### SERIALIZADOR ###
class TareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Tarea """
    plazo_tarea = serializers.CharField(read_only=True)
    progreso_tarea = serializers.CharField(read_only=True)
    class Meta:
        model = Tarea
        fields = ['id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_inicio','fecha_limite','plazo_tarea','progreso_tarea','creador_tarea']
        read_only_Fields = ('id')

    
    