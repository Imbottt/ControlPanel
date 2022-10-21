from unicodedata import name
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.models import User,Rol
from rol.serializers import RolSerializer

### SERIALIZADORES ###

### USUARIO ###
class UserSerializer(serializers.ModelSerializer):
    """ Serializador para el objeto de usuarios """

    class Meta:
        model = get_user_model()
        fields = ('email','password','name','last_name','rol_id','dir_id')
        extra_kwargs = {
            'password':{
                'write_only': True, 'min_length':5
                }
            }

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
        fields = ('email','password','is_administrador')
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
        fields = ('email','name','last_name','rol_id','dir_id')


################################
####### CRUD DEL USUARIO #######
################################


#### SERIALIZADOR QUE MUESTRA USUARIOS == list() ####
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'email': instance['email'],
            'name': instance['name'],
            'last_name': instance['last_name'],
            'rol_id': instance['rol_id'],
            'dir_id': instance['dir_id']
        }

### SERIALIZADOR QUE ACTUALIZA USUARIO ###
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email','name','last_name','rol_id','dir_id')