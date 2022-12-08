###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import UserTSubTarea
### Serializadores ###
from UserTSubTarea.serializers import UserTSubTareaSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
###
from django_filters.rest_framework import DjangoFilterBackend
### Capturar errores ###
from django.db import IntegrityError

##################################
## CRUD USER - TAREA - TAREASUB ##
##################################

####################################################################################

class UserTSubTareaCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista los USER - TAREA - TAREASUB que existen en la BD """
    serializer_class = UserTSubTareaSerializer
    queryset = UserTSubTareaSerializer.Meta.model.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_padre','userTarea','tarea','user']

    # Función para crear nuevos USER - TAREA - TAREASUB
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Ese USER - TAREA - TAREASUB ya existe')
                return Response({'error': e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class UserTSubTareaRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye los USER - TAREA - TAREASUB que existen en la BD """
    serializer_class = UserTSubTareaSerializer

    # Consulta para traer todos los USER - TAREA - TAREASUB que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene una USER - TAREA - TAREASUB en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            unidad_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(unidad_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe esa USER - TAREA - TAREASUB'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza una USER - TAREA - TAREASUB en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            unidad_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if unidad_serializer.is_valid():
                unidad_serializer.save()
                return Response({'message':'USER - TAREA - TAREASUB actualizada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar esa USER - TAREA - TAREASUB, no existe'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina una USER - TAREA - TAREASUB en específico
    def delete(self, request, pk=None):
        unidad_destroy = self.get_queryset().filter(id = pk).first()

        if unidad_destroy:
            unidad_destroy.delete()
            return Response({'message':'USER - TAREA - TAREASUB eliminado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar esa USER - TAREA - TAREASUB, no existe'}, status = status.HTTP_400_BAD_REQUEST)