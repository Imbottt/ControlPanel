###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

### Modelo de la BD ###
from core.models import Cargo

### Serializadores ###
from cargo.serializers import CargoSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
### Capturar errores ###
from django.db import IntegrityError

################
## CRUD CARGO ##
################
 
####################################################################################

class CargoCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista los cargos que existen en la BD """
    serializer_class = CargoSerializer
    queryset = CargoSerializer.Meta.model.objects.all()

    # Función para crear nuevos cargos
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {'Cargo': serializer.data,
                    'message':'Cargo creado correctamente'
                    }, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Esa cargo ya existe')
                return Response({'error': e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class CargoRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye los cargos que existen en la BD """
    serializer_class = CargoSerializer

    # Consulta para traer todos los cargos que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene un cargo en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            cargo_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(cargo_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe ese cargo'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Actualiza un cargo en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            cargo_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if cargo_serializer.is_valid():
                cargo_serializer.save()
                return Response({'message':'Cargo actualizada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede actualizar ese cargo, no existe'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina un cargo en específico
    def delete(self, request, pk=None):
        destroy = self.get_queryset().filter(id = pk).first()

        if destroy:
            destroy.delete()
            return Response({'message':'Cargo eliminado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede eliminar ese cargo, no existe'}, status = status.HTTP_400_BAD_REQUEST)