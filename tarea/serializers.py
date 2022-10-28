from rest_framework import serializers
from core.models import Tarea

### SERIALIZADOR ###
class TareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Tarea """
    plazo_tarea = serializers.CharField(read_only=True)
    progreso_tarea = serializers.CharField(read_only=True)
    class Meta:
        model = Tarea
        fields = ['id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_inicio','fecha_limite','plazo_tarea','progreso_tarea','estado_tarea']
        read_only_Fields = ('id','plazo_tarea','progreso_tarea',)

    def create(self, validated_data):
        return Tarea.objects.create(**validated_data)

    def get_fecha_fin(self, obj):
        return obj.fecha_limite.aggregate("fecha_limite")

    def get_fecha_hoy(self, obj):
        return obj.datetime.now().strftime('%d-%m-%Y %H:%M:%S').aggregate("fecha_hoy")

    def get_progreso(self, obj):
        return obj.progreso_tarea.aggregate(progreso= "fecha_limite" - "fecha_hoy")
    
    