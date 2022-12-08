###
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
### Modelo de la BD ###
from core.models import UserTarea
### Serializadores ###
from userTarea.serializers import UserTareaSerializer
### 
from rest_framework.response import Response
from rest_framework import status, generics
###
from django_filters.rest_framework import DjangoFilterBackend
### Capturar errores ###
from django.db import IntegrityError

#####################
## CRUD USER-TAREA ##
#####################

####################################################################################

class UserTareaCreateListApiView(generics.ListCreateAPIView):
    """ Una vista que crea y lista los usuarios y tareas que existen en la BD """
    serializer_class = UserTareaSerializer
    queryset = UserTareaSerializer.Meta.model.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user','tarea','estado_tarea','asignador']

    # Función para asignar una tarea a un usuario
    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            except IntegrityError as e:
                e = ('Esa tarea ya fue asignada')
                return Response({'error': e}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

####################################################################################

class UserTareaRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """ Una vista que busca, actualiza y destruye las tarea que están enlazadas a un usuario y que existen en la BD """
    serializer_class = UserTareaSerializer

    # Consulta para traer todos las tareas asignadas al usuario y que existen en la BD
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    # Obtiene una tarea y su usuario asignado en específico
    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            userT_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(userT_serializer.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe esa tarea y el usuario asignado a ella'}, status = status.HTTP_400_BAD_REQUEST)
    
    # Reasigna una tarea a un usuario existente en específico
    def put(self, request, pk=None):
        if self.get_queryset(pk):
            userT_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if userT_serializer.is_valid():
                userT_serializer.save()
                return Response({'message':'Tarea reasignada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede reasignar la tarea, no existe la tarea o el usuario'}, status = status.HTTP_400_BAD_REQUEST)

    # Elimina una asignación de tarea de un usuario en específico
    def delete(self, request, pk=None):
        destroy = self.get_queryset().filter(id = pk).first()

        if destroy:
            destroy.delete()
            return Response({'message':'Asignación de tarea eliminada correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No se puede reasignar la tarea, no existe la tarea o el usuario'}, status = status.HTTP_400_BAD_REQUEST)