###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import Direccion
### Serializadores ###
from direccion.serializers import DirSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
###

####################
## CRUD DIRECCIÓN ##
####################

####################################################################################

class DirCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista las direcciones que existen en la BD """
    serializer_class = DirSerializer
    queryset = DirSerializer.Meta.model.objects.all()

    # Función para crear nuevas direcciones
    def post(self, request):
        dir_serializer = self.serializer_class(data = request.data)

        if dir_serializer.is_valid():
            dir_serializer.save()
            return Response({'message':'Dirección creada correctamente'}, status = status.HTTP_201_CREATED)
        return Response(dir_serializer.data, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class DirRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye las direcciones que existen en la BD """
    serializer_class = DirSerializer

    # Consulta para traer todos los roles que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene una dirección en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            dir_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(dir_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe esa dirección'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza una dirección en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            dir_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if dir_serializer.is_valid():
                dir_serializer.save()
                return Response({'message':'Dirección actualizada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar esa dirección, no existe'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Elimina una dirección en específico
    def delete(self, request, pk=None):
        dir_destroy = self.get_queryset().filter(id = pk).first()
        if dir_destroy:
            dir_destroy.delete()
            return Response({'message':'Dirección eliminado correctamente'}, status = status.HTTP_200_OK)
        else:
            return Response({'error':'No se puede eliminar la dirección, no existe'}, status = status.HTTP_400_BAD_REQUEST)
        


