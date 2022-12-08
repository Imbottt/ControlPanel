###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import Rol
### Serializadores ###
from rol.serializers import RolSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics, authentication, permissions
### Capturar errores ###
from django.db import IntegrityError

##############
## CRUD ROL ##
##############

####################################################################################

class RolCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista los roles que existen en la BD """
    ################################
    # PERMISOS
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    ################################
    serializer_class = RolSerializer
    queryset = RolSerializer.Meta.model.objects.all()

    # Función para crear nuevos roles
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {'Rol': serializer.data,
                    'message':'Rol creado correctamente'
                    }, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Esa rol ya existe')
                return Response({'error':e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class RolRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye los roles que existen en la BD """
    ################################
    # PERMISOS
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    ################################
    serializer_class = RolSerializer

    # Consulta para traer todos los roles que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()
 
    # Obtiene un rol en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            rol_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(rol_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese rol'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza un rol en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            rol_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if rol_serializer.is_valid():
                rol_serializer.save()
                return Response({'message':'Rol actualizado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar ese rol, no existe'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina un rol en específico
    def delete(self, request, pk=None):
        rol_destroy = self.get_queryset().filter(id = pk).first()

        if rol_destroy:
            rol_destroy.delete()
            return Response({'message':'Rol eliminado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar el rol, no existe'}, status = status.HTTP_400_BAD_REQUEST)
        


