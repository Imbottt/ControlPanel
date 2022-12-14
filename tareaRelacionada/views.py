###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import TareaRelacionada
### Serializadores ###
from tareaRelacionada.serializers import TareaRelSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
### Capturar errores ###
from django.db import IntegrityError

############################
## CRUD TAREA RELACIONADA ##
############################

####################################################################################

class TareaRelCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista las tareas relacionadas que existen en la BD """
    serializer_class = TareaRelSerializer
    queryset = TareaRelSerializer.Meta.model.objects.all()

    # Función para crear nuevas tareas relacionadas
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Esa tarea relacionada ya existe')
                return Response({'error': e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class TareaRelRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye las tareas relacionadas que existen en la BD """
    serializer_class = TareaRelSerializer

    # Consulta para traer todos las tareas relacionadas que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene una tarea relacionada en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            flujo_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(flujo_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe esa tarea relacionada'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza una tarea relacionada en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            flujo_serializer = self.serializer_class(self.get_queryset(pk), data = request.data) 
            if flujo_serializer.is_valid():
                flujo_serializer.save()
                return Response({'message':'Tarea relacionada actualizado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar esa tarea relacionada, no existe'}, status = status.HTTP_400_BAD_REQUEST)
 
    # Elimina una tarea relacionada en específico
    def delete(self, request, pk=None):
        flujo_destroy = self.get_queryset().filter(id = pk).first()

        if flujo_destroy:
            flujo_destroy.delete()
            return Response({'message':'Tarea relacionada eliminada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar esa tarea relacionada, no existe'}, status = status.HTTP_400_BAD_REQUEST)