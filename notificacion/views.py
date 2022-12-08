###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import Notificacion
### Serializadores ###
from notificacion.serializers import NotifySerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
### Capturar errores ###
from django.db import IntegrityError

#######################
## CRUD NOTIFICACION ##
#######################

####################################################################################

class NotifyCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista los flujos que existen en la BD """
    serializer_class = NotifySerializer
    queryset = NotifySerializer.Meta.model.objects.all()

    # Función para crear nuevas notificaciones
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {'Notificación': serializer.data,
                    'message':'Notificación creada correctamente'
                    }, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Esa notificación ya existe')
                return Response({'error': e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class NotifyRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye los flujos que existen en la BD """
    serializer_class = NotifySerializer

    # Consulta para traer todos las notificaciones que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene una notificacion en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            flujo_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(flujo_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe esa notificación'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza una notificacion en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            flujo_serializer = self.serializer_class(self.get_queryset(pk), data = request.data) 
            if flujo_serializer.is_valid():
                flujo_serializer.save()
                return Response({'message':'Notificación actualizado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar esa notificación, no existe'}, status = status.HTTP_400_BAD_REQUEST)
 
    # Elimina una notificacion en específico
    def delete(self, request, pk=None):
        flujo_destroy = self.get_queryset().filter(id = pk).first()

        if flujo_destroy:
            flujo_destroy.delete()
            return Response({'message':'Notificación eliminada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar esa notificación, no existe'}, status = status.HTTP_400_BAD_REQUEST)