from rest_framework import serializers
from core.models import Direccion


### SERIALIZADOR ###
class DirSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Dirección """
    class Meta:
        model = Direccion
        fields = ('id','dir_name')
        read_only_Fields = ('id',)