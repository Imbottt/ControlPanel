###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import Unidad
### Serializadores ###
from unidad.serializers import UnidadSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
### Capturar errores ###
from django.db import IntegrityError

#################
## CRUD UNIDAD ##
#################

####################################################################################

class UnidadCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista las unidades que existen en la BD """
    serializer_class = UnidadSerializer
    queryset = UnidadSerializer.Meta.model.objects.all()

    # Función para crear nuevas unidades
    def post(self, request):
        dir_serializer = self.serializer_class(data = request.data)
        if dir_serializer.is_valid():
            try:
                dir_serializer.save()
                return Response(dir_serializer.data, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Esa unidad ya existe')
                return Response({'error':e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(dir_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class UnidadRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye las unidades que existen en la BD """
    serializer_class = UnidadSerializer

    # Consulta para traer todos las unidades que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene una unidad en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            unidad_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(unidad_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe esa unidad'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza una unidad en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            unidad_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if unidad_serializer.is_valid():
                unidad_serializer.save()
                return Response({'message':'Unidad actualizada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar la unidad, no existe'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina una unidad en específico
    def delete(self, request, pk=None):
        unidad_destroy = self.get_queryset().filter(id = pk).first()

        if unidad_destroy:
            unidad_destroy.delete()
            return Response({'message':'Unidad eliminado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar la unidad, no existe'}, status = status.HTTP_400_BAD_REQUEST)