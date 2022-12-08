from ast import Not
import email
from unicodedata import name
from urllib import request
from user import serializers
import user
from user.serializers import (
    SuperUserSerializer, 
    UserSerializer, 
    AuthTokenSerializer, 
    UserTokenSerializer,
    UpdateUserSerializer)
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

### Modelo de la BD ###
from core.models import User
### Serializadores ###
from user.serializers import UserSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
###

from django.shortcuts import get_object_or_404

from django.contrib.sessions.models import Session
from datetime import datetime

from core.models import User

### VISTAS ###

# Super Usuario
class CreateSuperUserView(generics.CreateAPIView):
    """ Crear un Super usuario == Administrador """
    # PERMISOS
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SuperUserSerializer


### LOGIN ###
class Login(ObtainAuthToken):
    # PERMISOS
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data = request.data, context = {'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user = user)
                user_serializer = UserTokenSerializer(user)
                if created: 
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message':'Inicio de sesión exitoso'
                    }, status = status.HTTP_201_CREATED)
                else:
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message':'Inicio de sesión exitoso'
                    }, status = status.HTTP_201_CREATED)
            else:
                return Response({'error':'Este usuario no puede iniciar sesión'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error':'Nombre de usuario o contraseña incorrecto'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({
            'token': token.key,
            'user': user_serializer.data,
            'message': 'Inicio de sesión exitoso'
            },status = status.HTTP_200_OK)

#### LOGOUT ####
class Logout(APIView):
    """ Salir de la aplicación """
    # PERMISOS
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()

            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())

                if all_sessions.exists():

                    for session in all_sessions:
                        session_data = session.get_decoded()

                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()

                session_message = 'Sesiones de usuario eliminadas'
                token_message = 'Token eliminado'
                return Response({'token_message': token_message, 'session_message': session_message}, 
                                    status = status.HTTP_200_OK)
                                
            return Response({'error':'No se ha encontrado un usuario con estas credenciales'},
                                    status = status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error':'No se ha encontrado token en la petición'},
                                    status = status.HTTP_409_CONFLICT)

###############
## CRUD USER ##
###############

####################################################################################
class UserCreateListApiView(generics.ListCreateAPIView):
    # PERMISOS
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    """ Una vista que crea y lista los usuarios que existen en la BD """
    serializer_class = UserSerializer
    queryset = UserSerializer.Meta.model.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['creador', 'rol', 'unidad']
 
    # Función para crear nuevos usuarios
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Usuario creado correctamente'
            }, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class UserRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    # PERMISOS
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)
    """ Una vista que busca, actualiza y destruye los usuarios que existen en la BD """
    serializer_class = UserSerializer

    # Consulta para traer todos los usuarios que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene un usuario en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            user_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(user_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese usuario'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza un usuario en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            user_serializer = UpdateUserSerializer(self.get_queryset(pk), data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'message':'Usuario actualizado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar ese usuario, no existe'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina un usuario en específico
    def delete(self, request, pk=None):
        destroy = self.get_queryset().filter(id = pk).first()

        if destroy:
            destroy.delete()
            return Response({'message':'Usuario eliminado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar ese usuario, no existe'}, status = status.HTTP_400_BAD_REQUEST)

###########################################################################################################