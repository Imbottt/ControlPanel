from unicodedata import name
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.models import User, Rol, Cargo, Unidad, Direccion

### SERIALIZADORES ###
####
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
#####

### USUARIO ###
class UserSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto de usuarios """
    class Meta:
        model = get_user_model()
        fields = ('id','email','password','name','last_name','creador','rol','cargo','unidad')
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

    def create(self, validated_data):
        """ Crear nuevo usuario con clave encriptada y retornarlo """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Actualiza al usuario, configura el password correctamente y lo retorna """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


### SUPERUSUARIO ###
class SuperUserSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto de superusuarios """
    class Meta:
        model = get_user_model()
        fields = ('email','password')
        extra_kwargs = {
            'password':{
                'write_only': True, 'min_length':5
                }
            }
    
    def create(self, validated_data):
        """ Crear nuevo usuario con clave encriptada y retornarlo """
        return get_user_model().objects.create_superuser(**validated_data)


### TOKEN DE AUTENTICACIÓN ###
class AuthTokenSerializer(serializers.Serializer):
    """ Serializador para el objeto de autentificación """
    email = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type' : 'password'},
        trim_whitespace = False
    )

    def validate(self, attrs):
        """ Validar y autentificar usuario """
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password = password
        )

        if not user:
            msg = _('Error: No se puede autentificar con estas credenciales')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

#### USER TOKEN ####
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','name','last_name','creador','rol','cargo','unidad')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['rol'] = RolSerializer(instance.rol).data
        response['cargo'] = CargoSerializer(instance.cargo).data
        response['unidad'] = UnidadSerializer(instance.unidad).data
        return response

### ACTUALIZAR USUARIO ###
class UpdateUserSerializer(serializers.ModelSerializer):
    """ Serializador que actualiza a los usuarios sin pedir contraseña """
    class Meta:
        model = get_user_model()
        fields = ['id','email','name','last_name','creador','rol','cargo','unidad']
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['rol'] = RolSerializer(instance.rol).data
        response['cargo'] = CargoSerializer(instance.cargo).data
        response['unidad'] = UnidadSerializer(instance.unidad).data
        return response

