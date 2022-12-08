###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import TareaSubordinada
### Serializadores ###
from subTarea.serializers import SubTareaSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
### Capturar errores ###
from django.db import IntegrityError

############################
## CRUD TAREA SUBORDINADA ##
############################

####################################################################################

class SubTareaCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista las tareas subordinada que existen en la BD """
    serializer_class = SubTareaSerializer
    queryset = SubTareaSerializer.Meta.model.objects.all()

    # Función para crear nuevas tareas subordinadas
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {'Reporte': serializer.data,
                    'message':'Tarea subordinada creada correctamente'
                    }, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Esa tarea subordinada ya existe')
                return Response({'error': e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class SubTareaRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye las tareas subordinadas que existen en la BD """
    serializer_class = SubTareaSerializer

    # Consulta para traer todas las tareas subordinadas que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene una tarea subordinada en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            subtarea_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(subtarea_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe esa tarea subordinada'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza una tarea subordinada en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            subtarea_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if subtarea_serializer.is_valid():
                subtarea_serializer.save()
                return Response({'message':'Tarea subordinada actualizada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar esa tarea subordinada, no existe'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina una tarea subordinada en específico
    def delete(self, request, pk=None):
        subtarea_destroy = self.get_queryset().filter(id = pk).first()

        if subtarea_destroy:
            subtarea_destroy.delete()
            return Response({'message':'Tarea subordinada eliminada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar esa tarea subordinada, no existe'}, status = status.HTTP_400_BAD_REQUEST)
        


