###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import Flujo
### Serializadores ###
from flujo.serializers import FlujoSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
###

##############
## CRUD ROL ##
##############

####################################################################################

class FlujoCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista los flujos que existen en la BD """
    serializer_class = FlujoSerializer
    queryset = FlujoSerializer.Meta.model.objects.all()

    # Función para crear nuevos flujos
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Flujo creado correctamente'
            }, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class FlujoRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye los flujos que existen en la BD """
    serializer_class = FlujoSerializer

    # Consulta para traer todos los flujos que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene un flujo en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            flujo_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(flujo_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese flujo'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza un flujo en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            flujo_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if flujo_serializer.is_valid():
                flujo_serializer.save()
                return Response({'message':'flujo actualizado correctamente'}, status = status.HTTP_200_OK)
            return Response({'error':'No existe ese flujo'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina un flujo en específico
    def delete(self, request, pk=None):
        flujo_destroy = self.get_queryset().filter(id = pk).first()

        if flujo_destroy:
            flujo_destroy.delete()
            return Response({'message':'flujo eliminado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese flujo'}, status = status.HTTP_400_BAD_REQUEST)
        


