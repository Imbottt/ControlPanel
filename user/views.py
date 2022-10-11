import email
from unicodedata import name
from user.serializers import UserSerializer, AuthTokenSerializer, UserTokenSerializer
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings

from django.contrib.sessions.models import Session
from datetime import datetime

### VISTAS ###

class CreateUserView(generics.CreateAPIView):
    """ Crear nuevo usuario en el sistema """
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """ Crear nuevo token para el usuario """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manejar el usuario autenticado """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """ Obtener y retornar usuario autenticado """
        return self.request.user

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

        