from rest_framework import serializers
from core.models import Direccion

### SERIALIZADOR ###
class DirSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Dirección """
    class Meta:
        model = Direccion
        fields = ['id','dir_name']
        read_only_Fields = ('id',)
        extra_kwargs = {
            'dir_name':{
                'min_length': 4,
                }
            }

    def validate_dir(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar un valor en el campo vacío")
        return value
