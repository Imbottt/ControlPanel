from rest_framework import serializers
from core.models import UserFlujo, Flujo, Rol, Cargo, Unidad, Direccion
from django.contrib.auth import get_user_model # --> User --> Modelo User de la BD

### SERIALIZADOR PARA EL ROL ###
class RolSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Rol
        fields = ['id','rol_name']
        read_only_Fields = ('id',)

### SERIALIZADOR PARA EL CARGO ###
class CargoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Cargo """
    class Meta:
        model = Cargo
        fields = ['id','cargo_name']
        read_only_Fields = ('id',)

#####
### SERIALIZADOR DE DIRECCIÓN ###
class DirSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Dirección """
    class Meta:
        model = Direccion
        fields = ['id','dir_name']
        read_only_Fields = ('id',)

### SERIALIZADOR DE UNIDAD ###
class UnidadSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = Unidad
        fields = ['id','unidad_name','dir']
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['dir'] = DirSerializer(instance.dir).data
        return response

### USUARIO ###
class UserSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto de usuarios """
    class Meta:
        model = get_user_model()
        fields = ['id','email','name','last_name','rol','cargo','unidad']
        read_only_Fields = ('id',)

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
        fields = ['id','flujo_name','descripcion_flujo','fecha_creacion','fecha_inicio','fecha_fin','plazo_flujo','creador_flujo','ejecutar']
        read_only_Fields = ('id',)

### SERIALIZADOR PARA USER-TAREA###
class UserFlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto UserTarea """
    class Meta:
        model = UserFlujo
        fields = ['id','user','flujo','asignador']
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['flujo'] = FlujoSerializer(instance.flujo).data
        response['user'] = UserSerializer(instance.user).data
        return response