###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import RegistroEjecucion
### Serializadores ###
from registroEjecucion.serializers import RegistroExeSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
### Capturar errores ###
from django.db import IntegrityError

#############################
## CRUD REGISTRO EJECUCIÓN ##
#############################

####################################################################################

class RegistroExeCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista los registros de ejecución que existen en la BD """
    serializer_class = RegistroExeSerializer
    queryset = RegistroExeSerializer.Meta.model.objects.all()

    # Función para crear nuevos registros de ejecución
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {'Registro de ejecución de tareas': serializer.data,
                    'message':'Registro de ejecución de tareas creado correctamente'
                    }, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Ese registro de ejecución de tareas ya existe')
                return Response({'error': e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class RegistroExeRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye los registro de ejecución que existen en la BD """
    serializer_class = RegistroExeSerializer

    # Consulta para traer todos los registro de ejecución que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene un registro de ejecución en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            flujo_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(flujo_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese registro de ejecución'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza un registro de ejecución en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            flujo_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if flujo_serializer.is_valid():
                flujo_serializer.save()
                return Response({'message':'Registro de ejecución actualizado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar ese registro de ejecución, no existe'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina un registro de ejecución en específico
    def delete(self, request, pk=None):
        flujo_destroy = self.get_queryset().filter(id = pk).first()

        if flujo_destroy:
            flujo_destroy.delete()
            return Response({'message':'Registro de ejecución eliminado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar ese registro de ejecución, no existe'}, status = status.HTTP_400_BAD_REQUEST)