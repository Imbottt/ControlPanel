from rest_framework import serializers
from core.models import Flujo


### SERIALIZADOR PARA EL FLUJO ###
class FlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Flujo """
    class Meta:
        model = Flujo
        fields = ('id','titulo_flujo')
        read_only_Fields = ('id',)
