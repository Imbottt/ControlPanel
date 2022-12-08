###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import RegistroFlujo
### Serializadores ###
from registroFlujo.serializers import RegFluSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
### Capturar errores ###
from django.db import IntegrityError

#############################
## CRUD REGISTRO EJECUCIÓN ##
#############################

####################################################################################

class RegFluCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista los registros de flujos que existen en la BD """
    serializer_class = RegFluSerializer
    queryset = RegFluSerializer.Meta.model.objects.all()

    # Función para crear nuevos registros de flujos
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {'Registro de ejecución de flujos': serializer.data,
                    'message':'Registro de ejecución de flujos creado correctamente'
                    }, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Ese registro de ejecución de flujos ya existe')
                return Response({'error': e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class RegFluRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye los registro de flujo que existen en la BD """
    serializer_class = RegFluSerializer

    # Consulta para traer todos los registro de flujo que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene un registro de flujo en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            flujo_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(flujo_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese registro de flujos'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza un registro de flujo en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            flujo_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if flujo_serializer.is_valid():
                flujo_serializer.save()
                return Response({'message':'Registro de flujo actualizado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar ese registro de flujo, no existe'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina un registro de flujo en específico
    def delete(self, request, pk=None):
        flujo_destroy = self.get_queryset().filter(id = pk).first()

        if flujo_destroy:
            flujo_destroy.delete()
            return Response({'message':'Registro de flujo eliminado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar ese registro de flujo, no existe'}, status = status.HTTP_400_BAD_REQUEST)