from django.shortcuts import render

# Create your views here.
from importlib.util import resolve_name
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from core.models import Unidad

from unidad.serializers import UnidadSerializer, UnidadListSerializer, UpdateUnidadSerializer

###
from rest_framework.response import Response
from rest_framework import status
###


#################
## CRUD UNIDAD ##
#################

class UnidadViewSet(viewsets.GenericViewSet):
    model = Unidad
    serializer_class = UnidadSerializer
    list_serializer_class = UnidadListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)
        

    # CONSULTA PARA OBTENER TODOS LOS ROLES DE LA BD #
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.values('id','unidad_name')
            return self.queryset

    # LISTA LOS ROLES EXISTENTES EN LA BD #
    def list(self,request):
        unidad = self.get_queryset()
        unidad_serializer = self.list_serializer_class(unidad, many=True)
        return Response(unidad_serializer.data, status=status.HTTP_200_OK)

    # CREA NUEVOS ROLES #
    def create(self, request):
        unidad_serializer = self.serializer_class(data=request.data)
        if unidad_serializer.is_valid():
            unidad_serializer.save()
            return Response({
                'message':'Unidad creada correctamente'
            }, status = status.HTTP_201_CREATED)
        return Response({
            'message':'Hay errores en el momento de crear una unidad',
            'errors':unidad_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # RETORNA LA INFORMACIÓN DE UN ROL ESPECIFICO #
    def retrieve(self, request, pk=None):
        unidad = self.get_object(pk)
        unidad_serializer = self.serializer_class(unidad)
        return Response(unidad_serializer.data)

    # ACTUALIZA A LOS ROL # 
    def update(self, request, pk=None):
        unidad = self.get_object(pk)
        unidad_serializer = UpdateUnidadSerializer(unidad, data = request.data)
        if unidad_serializer.is_valid():
            unidad_serializer.save()
            return Response({
                'message':'Unidad actualizada correctamente'
            },status = status.HTTP_200_OK)

        return Response({
            'message':'Hay errores en la actualizaciones',
            'errors':unidad_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # ELIMINA A LOS ROL #
    def destroy(self, request, pk=None):
        unidad_destroy = self.model.objects.filter(id=pk).update('unidad_name')
        if unidad_destroy == 1:
            return Response({
                'message':'Unidad eliminada correctamente'
            },status = status.HTTP_200_OK)
        return Response({
            'message':'No existe la unidad que desea eliminar'
        },status = status.HTTP_404_NOT_FOUND)