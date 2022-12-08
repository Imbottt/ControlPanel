###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import Tarea
### Serializadores ###
from tarea.serializers import TareaSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
### Capturar errores ###
from django.db import IntegrityError

################
## CRUD TAREA ##
################

####################################################################################

class TareaCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista las tareas que existen en la BD """
    ################################
    # PERMISOS
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    ################################
    serializer_class = TareaSerializer
    queryset = TareaSerializer.Meta.model.objects.all()

    # Función para crear nuevas tareas
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Esa tarea ya existe')
                return Response({'error': e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class TareaRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye las tareas que existen en la BD """
    serializer_class = TareaSerializer

    # Consulta para traer todas las tareas que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene una tarea en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            tarea_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(tarea_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe esa tarea'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza una tarea en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            tarea_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if tarea_serializer.is_valid():
                tarea_serializer.save()
                return Response({'message':'Tarea actualizada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar esa tarea, no existe'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina una tarea en específico
    def delete(self, request, pk=None):
        tarea_destroy = self.get_queryset().filter(id = pk).first()

        if tarea_destroy:
            tarea_destroy.delete()
            return Response({'message':'Tarea eliminada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar esa tarea, no existe'}, status = status.HTTP_400_BAD_REQUEST)
        


