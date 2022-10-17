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
    UserListSerializer,
    UpdateUserSerializer)
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from django.contrib.sessions.models import Session
from datetime import datetime

from core.models import User

### VISTAS ###

    # PERMISOS
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.IsAuthenticated,)

# Super Usuario
class CreateSuperUserView(generics.CreateAPIView):
    """ Crear un Super usuario == Administrador """
    serializer_class = SuperUserSerializer


### LOGIN ###
class Login(ObtainAuthToken):

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

#### CREAR USUARIO ####
class UserViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    
    # CONSULTA PARA OBTENER TODOS LOS USUARIOS DE LA BD #
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects\
                            .filter(is_active=True)\
                            .values('id','email','name','last_name','rol_id','is_active')
            return self.queryset


    # LISTA LOS USUARIOS CON SUS ATRIBUTOS #
    def list(self,request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)


    # CREA NUEVOS USUARIOS #
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message':'Usuario creado correctamente'
            }, status = status.HTTP_201_CREATED)
        return Response({
            'message':'Hay errores en el registro',
            'errors':user_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # RETORNA LA INFORMACIÓN DE UN USUARIO ESPECIFICO #
    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data)

    # ACTUALIZA A LOS USUARIOS # 
    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateUserSerializer(user, data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message':'Usuario actualizado correctamente'
            },status = status.HTTP_200_OK)

        return Response({
            'message':'Hay errores en la actualizaciones',
            'errors':user_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # ELIMINA A LOS USUARIOS #
    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response({
                'message':'Usuario eliminado correctamente'
            },status = status.HTTP_200_OK)
        return Response({
            'message':'No existe el usuario que desea eliminar'
        },status = status.HTTP_404_NOT_FOUND)

