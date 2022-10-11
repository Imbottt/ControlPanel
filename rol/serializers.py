from rest_framework import serializers
from core.models import Roll 


### SERIALIZADOR ###
class RolSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Roll
        fields = ('id','rol_name')
        read_only_Fields = ('id',)