from rest_framework import serializers
from core.models import Reporte


### SERIALIZADOR PARA LA ALERTA ###
class ReporteSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto alerta """
    class Meta:
        model = Reporte
        fields = ('id','id_reportador_rechazador','justificacion','is_reported','tarea','asignador_tarea')
        read_only_Fields = ('id',)