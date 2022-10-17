from importlib.util import resolve_name
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from core.models import TareaSubordinada

from subTarea.serializers import SubTareaSerializer, SubTareaListSerializer, UpdateSubTareaSerializer

###
from rest_framework.response import Response
from rest_framework import status
###


############################
## CRUD TAREA SUBORDINADA ##
############################

class SubTareaViewSet(viewsets.GenericViewSet):
    model = TareaSubordinada
    serializer_class = SubTareaSerializer
    list_serializer_class = SubTareaListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)
        

    # CONSULTA PARA OBTENER TODAS LAS TAREAS SUBORDINADAS DE LA BD #
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.values('id','titulo_tarea_sub','descripcion_tarea_sub')
            return self.queryset

    # LISTA LAS TAREAS SUBORDINADAS EXISTENTES EN LA BD #
    def list(self,request):
        subtareas = self.get_queryset()
        subtareas_serializer = self.list_serializer_class(subtareas, many=True)
        return Response(subtareas_serializer.data, status=status.HTTP_200_OK)

    # CREA NUEVAS TAREAS SUBORDINADAS #
    def create(self, request):
        subtarea_serializer = self.serializer_class(data=request.data)
        if subtarea_serializer.is_valid():
            subtarea_serializer.save()
            return Response({
                'message':'Tarea subordinada creada correctamente'
            }, status = status.HTTP_201_CREATED)
        return Response({
            'message':'Hay errores en el momento de crear la tarea subordinada',
            'errors':subtarea_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # RETORNA LA INFORMACIÓN DE UNA TAREA SUBORDINADA ESPECÍFICA #
    def retrieve(self, request, pk=None):
        subtarea = self.get_object(pk)
        subtarea_serializer = self.serializer_class(subtarea)
        return Response(subtarea_serializer.data)

    # ACTUALIZA A LAS TAREAS SUBORDINADAS # 
    def update(self, request, pk=None):
        subtarea = self.get_object(pk)
        subtarea_serializer = UpdateSubTareaSerializer(subtarea, data = request.data)
        if subtarea_serializer.is_valid():
            subtarea_serializer.save()
            return Response({
                'message':'Tarea subordinada actualizada correctamente'
            },status = status.HTTP_200_OK)

        return Response({
            'message':'Hay errores en la actualización de la tarea subordinada',
            'errors':subtarea_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # ELIMINA LAS TAREAS SUBORDINADAS #
    def destroy(self, request, pk=None):
        subtarea_destroy = self.model.objects.filter(id=pk).update('titulo_tarea_sub')
        if subtarea_destroy == 1:
            return Response({
                'message':'Tarea subordinada eliminada correctamente'
            },status = status.HTTP_200_OK)
        return Response({
            'message':'No existe la tarea subordinada que desea eliminar'
        },status = status.HTTP_404_NOT_FOUND)