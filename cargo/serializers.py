from rest_framework import serializers
from core.models import Cargo


### SERIALIZADOR PARA EL ROL ###
class CargoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto cargo """
    class Meta:
        model = Cargo
        fields = ('id','cargo_name')
        read_only_Fields = ('id',)