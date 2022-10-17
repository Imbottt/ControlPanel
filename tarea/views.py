from importlib.util import resolve_name
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from core.models import Tarea

from tarea.serializers import TareaSerializer, TareaListSerializer, UpdateTareaSerializer

###
from rest_framework.response import Response
from rest_framework import status
###


################
## CRUD TAREA ##
################

class TareaViewSet(viewsets.GenericViewSet):
    model = Tarea
    serializer_class = TareaSerializer
    list_serializer_class = TareaListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)
        

    # CONSULTA PARA OBTENER TODAS LAS TAREAS DE LA BD #
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.values('id','titulo_tarea','descripcion_tarea','fecha_creacion','fecha_limite','progreso_tarea')
            return self.queryset

    # LISTA LAS TAREAS EXISTENTES EN LA BD #
    def list(self,request):
        tareas = self.get_queryset()
        tareas_serializer = self.list_serializer_class(tareas, many=True)
        return Response(tareas_serializer.data, status=status.HTTP_200_OK)

    # CREA NUEVAS TAREAS #
    def create(self, request):
        tarea_serializer = self.serializer_class(data=request.data)
        if tarea_serializer.is_valid():
            tarea_serializer.save()
            return Response({
                'message':'Tarea creada correctamente'
            }, status = status.HTTP_201_CREATED)
        return Response({
            'message':'Hay errores en el momento de crear una tarea',
            'errors':tarea_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # RETORNA LA INFORMACIÓN DE UNA TAREA ESPECÍFICA #
    def retrieve(self, request, pk=None):
        tarea = self.get_object(pk)
        tarea_serializer = self.serializer_class(tarea)
        return Response(tarea_serializer.data)

    # ACTUALIZA LAS TAREAS # 
    def update(self, request, pk=None):
        tarea = self.get_object(pk)
        tarea_serializer = UpdateTareaSerializer(tarea, data = request.data)
        if tarea_serializer.is_valid():
            tarea_serializer.save()
            return Response({
                'message':'Tarea actualizada correctamente'
            },status = status.HTTP_200_OK)

        return Response({
            'message':'Hay errores en la creación de la tarea',
            'errors':tarea_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # ELIMINA A LAS TAREAS #
    def destroy(self, request, pk=None):
        tarea_destroy = self.model.objects.filter(id=pk).update('titulo_tarea')
        if tarea_destroy == 1:
            return Response({
                'message':'Tarea eliminada correctamente'
            },status = status.HTTP_200_OK)
        return Response({
            'message':'No existe la tarea que desea eliminar'
        },status = status.HTTP_404_NOT_FOUND)