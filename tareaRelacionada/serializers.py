from rest_framework import serializers
from core.models import TareaRelacionada

###
from datetime import datetime

### SERIALIZADOR ###
class TareaRelSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Tarea """
    class Meta:
        model = TareaRelacionada
        fields = ['id','id_tarea_main','id_tarea_relational']
        read_only_Fields = ('id',)