from ast import Delete, Not
from asyncio.windows_events import NULL
from importlib.util import resolve_name
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from core.models import Rol

from rol.serializers import RolSerializer, RolListSerializer, UpdateRolSerializer

###
from rest_framework.response import Response
from rest_framework import status
###


##############
## CRUD ROL ##
##############

class RolViewSet(viewsets.GenericViewSet):
    model = Rol
    serializer_class = RolSerializer
    list_serializer_class = RolListSerializer
    queryset = None

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response ({'message':'No existe'}, status = status.HTTP_400_BAD_REQUEST)
        

    # CONSULTA PARA OBTENER TODOS LOS ROLES DE LA BD #
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.values('id','rol_name')
            return self.queryset

    # LISTA LOS ROLES EXISTENTES EN LA BD #
    def list(self,request):
        rols = self.get_queryset()
        rols_serializer = self.list_serializer_class(rols, many=True)
        return Response(rols_serializer.data, status=status.HTTP_200_OK)

    # CREA NUEVOS ROLES #
    def create(self, request):
        rol_serializer = self.serializer_class(data=request.data)
        if rol_serializer.is_valid():
            rol_serializer.save()
            return Response({
                'message':'Rol creado correctamente'
            }, status = status.HTTP_201_CREATED)
        return Response({
            'message':'Hay errores en el momento de crear un rol',
            'errors':rol_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # RETORNA LA INFORMACIÓN DE UN ROL ESPECIFICO #
    def retrieve(self, request, pk=None):
        rol = self.get_object(pk)
        rol_serializer = self.serializer_class(rol)
        return Response(rol_serializer.data)

    # ACTUALIZA A LOS ROL # 
    def update(self, request, pk=None):
        rol = self.get_object(pk)
        rol_serializer = UpdateRolSerializer(rol, data = request.data)
        if rol_serializer.is_valid():
            rol_serializer.save()
            return Response({
                'message':'Rol actualizado correctamente'
            },status = status.HTTP_200_OK)

        return Response({
            'message':'Hay errores en la actualizaciones',
            'errors':rol_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # ELIMINA A LOS ROL #
    def destroy(self, request, pk=None):
        rol = self.get_object(pk)
        if rol == self.get_object(pk):
            return Response({
                'message':'Rol eliminado correctamente'
            },status = status.HTTP_200_OK)
        return Response({
            'message':'No existe el rol que desea eliminar'
        },status = status.HTTP_404_NOT_FOUND)