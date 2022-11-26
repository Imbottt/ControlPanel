from rest_framework import serializers
from core.models import UserTarea, Tarea, Rol, Cargo, Unidad, Direccion
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

### SERIALIZADOR ###
class TareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Tarea """
    class Meta:
        model = Tarea
        fields = ['id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_inicio','fecha_limite','progreso_tarea','creador_tarea']
        read_only_Fields = ('id',)

### SERIALIZADOR PARA USER-TAREA###
class UserTareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto UserTarea """
    class Meta:
        model = UserTarea
        fields = ['id','user','tarea','estado_tarea','asignador']
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tarea'] = TareaSerializer(instance.tarea).data
        response['user'] = UserSerializer(instance.user).data
        return response

