from rest_framework import serializers
from core.models import Notificacion, Tarea

###
from datetime import datetime

### SERIALIZADOR ###
class TareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Tarea """
    plazo_tarea = serializers.CharField(read_only=True)
    progreso_tarea = serializers.CharField(read_only=True)
    class Meta:
        model = Tarea
        fields = ['id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_inicio','fecha_limite','plazo_tarea','progreso_tarea','creador_tarea']
        read_only_Fields = ('id')


### SERIALIZADOR NOTIFICACION ###
class NotifySerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Flujo """
    class Meta:
        model = Notificacion
        fields = ['id','id_notificador','id_notificado','mensaje','fecha_creacion','is_read','tarea']
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tarea'] = TareaSerializer(instance.tarea).data
        return response
    