from rest_framework import serializers
from core.models import Reporte


### SERIALIZADOR PARA LA ALERTA ###
class ReporteSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto alerta """
    class Meta:
        model = Reporte
        fields = ('id','justificacion','tarea')
        read_only_Fields = ('id',)