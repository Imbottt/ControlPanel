###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

### Modelo de la BD ###
from core.models import Reporte

### Serializadores ###
from reporte.serializers import ReporteSerializer

### 
from rest_framework.response import Response
from rest_framework import status, generics
###
from django_filters.rest_framework import DjangoFilterBackend

##################
## CRUD REPORTE ##
##################

####################################################################################

class ReporteCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista los reportes que existen en la BD """
    serializer_class = ReporteSerializer
    queryset = ReporteSerializer.Meta.model.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_reportador_rechazador','is_reported','asignador_tarea']

    # Función para crear nuevos reportes
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class ReporteRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye los reportes que existen en la BD """
    serializer_class = ReporteSerializer

    # Consulta para traer todos los reportes que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene un reporte en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            alerta_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(alerta_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese reporte'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza un reporte en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            alter = self.serializer_class(self.get_queryset(pk), data = request.data)
            if alter.is_valid():
                alter.save()
                return Response({'message':'Reporte actualizada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar esa reporte, no existe'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina un reporte en específico
    def delete(self, request, pk=None):
        destroy = self.get_queryset().filter(id = pk).first()

        if destroy:
            destroy.delete()
            return Response({'message':'Reporte eliminada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar ese reporte, no existe'}, status = status.HTTP_400_BAD_REQUEST)