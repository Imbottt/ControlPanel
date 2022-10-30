from rest_framework import serializers
from core.models import Alertas


### SERIALIZADOR PARA EL ROL ###
class AlertaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto alerta """
    class Meta:
        model = Alertas
        fields = ('id','confirmacion','justificacion','tarea')
        read_only_Fields = ('id',)