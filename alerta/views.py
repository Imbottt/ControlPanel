###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

### Modelo de la BD ###
from core.models import Alertas

### Serializadores ###
from alerta.serializers import AlertaSerializer

### 
from rest_framework.response import Response
from rest_framework import status, generics
###

#################
## CRUD ALERTA ##
#################

####################################################################################

class AlertaCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista las alertas que existen en la BD """
    serializer_class = AlertaSerializer
    queryset = AlertaSerializer.Meta.model.objects.all()

    # Función para crear nuevas alertas
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Alerta creado correctamente'
            }, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class AlertaRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye las alertas que existen en la BD """
    serializer_class = AlertaSerializer

    # Consulta para traer todos las alertas que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene una alerta en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            alerta_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(alerta_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese cargo'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza un cargo en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            alter = self.serializer_class(self.get_queryset(pk), data = request.data)
            if alter.is_valid():
                alter.save()
                return Response({'message':'Alerta actualizada correctamente'}, status = status.HTTP_200_OK)
            return Response({'error':'No existe esa alerta'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina un cargo en específico
    def delete(self, request, pk=None):
        destroy = self.get_queryset().filter(id = pk).first()

        if destroy:
            destroy.delete()
            return Response({'message':'Alerta eliminada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No existe esa alerta'}, status = status.HTTP_400_BAD_REQUEST)