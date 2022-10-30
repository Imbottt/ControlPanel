from rest_framework import serializers
from core.models import Flujo, Rol, Unidad, Direccion, Cargo
from django.contrib.auth import get_user_model

### SERIALIZADOR PARA EL ROL ###
class RolSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Rol
        fields = ['rol_name']

### SERIALIZADOR PARA EL CARGO ###
class CargoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Cargo """
    class Meta:
        model = Cargo
        fields = ['cargo_name']

### SERIALIZADOR DE DIRECCIÓN ###
class DirSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Dirección """
    class Meta:
        model = Direccion
        fields = ['dir_name']

### SERIALIZADOR DE UNIDAD ###
class UnidadSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Unidad
        fields = ['unidad_name','dir']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['dir'] = DirSerializer(instance.dir).data
        return response

### USUARIO ###
class UserSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto de usuarios """
    class Meta:
        model = get_user_model()
        fields = ['email','name','last_name','rol','cargo','unidad']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['rol'] = RolSerializer(instance.rol).data
        response['cargo'] = CargoSerializer(instance.cargo).data
        response['unidad'] = UnidadSerializer(instance.unidad).data
        return response

### SERIALIZADOR PARA EL FLUJO ###
class FlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Flujo """
    class Meta:
        model = Flujo
        fields = ['id','flujo_name','descripcion_flujo','fecha_creacion','fecha_inicio','fecha_fin','user']
        read_only_Fields = ('id',)
