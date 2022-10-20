###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import Unidad
### Serializadores ###
from estadoTarea.serializers import EstadoTareaSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
###

#######################
## CRUD ESTADO TAREA ##
#######################

####################################################################################

class EstadoTareaCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista los estados de tarea que existen en la BD """
    serializer_class = EstadoTareaSerializer
    queryset = EstadoTareaSerializer.Meta.model.objects.all()

    # Función para crear nuevos estados
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Estado de tarea creado correctamente'
            }, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class EstadoTareaRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye los estados de tarea que existen en la BD """
    serializer_class = EstadoTareaSerializer

    # Consulta para traer todos los estados de tarea que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene un estado de tarea en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            estado_tarea_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(estado_tarea_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese estado de tarea'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza un estado de tarea en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            estado_tarea_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if estado_tarea_serializer.is_valid():
                estado_tarea_serializer.save()
                return Response(estado_tarea_serializer.data, status = status.HTTP_200_OK)
            return Response(estado_tarea_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    # Elimina un estado de tarea en específico
    def delete(self, request, pk=None):
        estado_tarea_destroy = self.get_queryset().filter(id = pk).first()

        if estado_tarea_destroy:
            estado_tarea_destroy.delete()
            return Response({'message':'Estado de tarea eliminado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese estado de tarea'}, status = status.HTTP_400_BAD_REQUEST)