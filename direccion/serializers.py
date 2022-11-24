from rest_framework import serializers
from core.models import Direccion

### SERIALIZADOR ###
class DirSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Dirección """
    dir_name = serializers.CharField(allow_null=False, required=True, allow_blank=False, min_length=4)
    
    class Meta:
        model = Direccion
        fields = ['id','dir_name']
        read_only_Fields = ('id',)

    
