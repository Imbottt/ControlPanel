from rest_framework import serializers
from core.models import Direccion

### SERIALIZADOR ###
class DirSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Dirección """

    # Validaciones de la dirección
    def is_valid_dir(value):
        if len(value) < 4:
            raise serializers.ValidationError("El largo del nombre no puede ser menor a 4 carácteres")
        elif len(value) < 0:
            raise serializers.ValidationError("El campo del nombre no puede estar vacío")

    dir_name = serializers.CharField(validators=[is_valid_dir])
    
    class Meta:
        model = Direccion
        fields = ['id','dir_name']
        read_only_Fields = ('id',)

    def create(self, validated_data):
        """ Crear nuevo usuario con clave encriptada y retornarlo """
        return  Direccion.objects.create(**validated_data)
        
    
     
   

