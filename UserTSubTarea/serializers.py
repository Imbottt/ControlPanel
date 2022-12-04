from rest_framework import serializers
from core.models import UserTSubTarea, Rol, Cargo, Direccion, Unidad, Tarea, TareaSubordinada, UserTarea
from django.contrib.auth import get_user_model

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
        fields = ('id','email','name','last_name','creador','rol','cargo','unidad')
        extra_kwargs = {
            'password':{
                'write_only': True, 'min_length':5
                }
            }

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
        read_only_Fields = ('id')

### SERIALIZADOR ###
class SubTareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto Rol """
    class Meta:
        model = TareaSubordinada
        fields = ('id','titulo_subTarea','descripcion_subTarea','fecha_creacion','fecha_inicio','fecha_fin','tarea')
        read_only_Fields = ('id',)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['tarea'] = TareaSerializer(instance.tarea).data
        return response
 
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

### SERIALIZADOR ###
class UserTSubTareaSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto User - Tarea - SubTarea """
    class Meta:
        model = UserTSubTarea
        fields = ['id','id_padre','userTarea','user','tarea','asignador']
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['userTarea'] = UserTareaSerializer(instance.userTarea).data
        response['user'] = UserSerializer(instance.user).data
        response['tarea'] = TareaSerializer(instance.tarea).data
        return response