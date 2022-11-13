from rest_framework import serializers
from core.models import UserTarea, Tarea, Rol, Cargo, Unidad, Direccion, RegistroEjecucion, UserFlujo, Flujo
from django.contrib.auth import get_user_model # --> User --> Modelo User de la BD

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

#####
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

### SERIALIZADOR ###
class TareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Tarea """
    plazo_tarea = serializers.CharField(read_only=True)
    progreso_tarea = serializers.CharField(read_only=True)
    class Meta:
        model = Tarea
        fields = ['id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_inicio','fecha_limite','plazo_tarea','progreso_tarea','creador_tarea']
        read_only_Fields = ('id','plazo_tarea','progreso_tarea',)

### SERIALIZADOR PARA EL FLUJO ###
class FlujoSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Flujo """
    plazo_flujo = serializers.CharField(read_only=True)
    class Meta:
        model = Flujo
        fields = ['id','flujo_name','descripcion_flujo','fecha_creacion','fecha_inicio','fecha_fin','plazo_flujo']
        read_only_Fields = ('id','fecha_creacion',)

### SERIALIZADOR PARA USER-TAREA###
class UserTareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto UserTarea """
    class Meta:
        model = UserTarea
        fields = ['id','user','tarea','estado_tarea','asignador']
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response['tarea'] = TareaSerializer(instance.tarea).data
        return response

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

### SERIALIZADOR REGISTRO EJECUCIÓN ###
class RegistroExeSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Registro de ejecución """
    class Meta:
        model = RegistroEjecucion
        fields = ['id','titulo_reg','fecha_reg','userTarea','userFlujo']
        read_only_Fields = ('id','fecha_reg',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['userTarea'] = UserTareaSerializer(instance.userTarea).data
        return response
