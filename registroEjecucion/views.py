from importlib.util import resolve_name
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from core.models import RegistroEjecucion

from registroEjecucion.serializers import RegistroExeSerializer, RegistroExeListSerializer, UpdateRegistroExeSerializer

###
from rest_framework.response import Response
from rest_framework import status
###


################################
## CRUD REGISTRO DE EJECUCIÓN ##
################################

class RolViewSet(viewsets.GenericViewSet):
    model = RegistroEjecucion
    serializer_class = RegistroExeSerializer
    list_serializer_class = RegistroExeListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)
        

    # CONSULTA PARA OBTENER TODOS LOS REGISTROS DE LA BD #
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.values('id','confirmacion','justificacion','observacion','fecha_registro')
            return self.queryset

    # LISTA LOS REGISTROS EXISTENTES EN LA BD #
    def list(self,request):
        regs_exe = self.get_queryset()
        regs_exe_serializer = self.list_serializer_class(regs_exe, many=True)
        return Response(regs_exe_serializer.data, status=status.HTTP_200_OK)

    # CREA NUEVOS REGISTROS #
    def create(self, request):
        regs_exe_serializer = self.serializer_class(data=request.data)
        if regs_exe_serializer.is_valid():
            regs_exe_serializer.save()
            return Response({
                'message':'Registro de ejecución creado correctamente'
            }, status = status.HTTP_201_CREATED)
        return Response({
            'message':'Hay errores en el momento de crear el registro de ejecución',
            'errors':regs_exe_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # RETORNA LA INFORMACIÓN DE UN REGISTRO DE EJECUCIÓN ESPECIFICO #
    def retrieve(self, request, pk=None):
        regs_exe = self.get_object(pk)
        regs_exe_serializer = self.serializer_class(regs_exe)
        return Response(regs_exe_serializer.data)

    # ACTUALIZA A LOS REGISTROS DE EJECUCIÓN # 
    def update(self, request, pk=None):
        regs_exe = self.get_object(pk)
        regs_exe_serializer = UpdateRegistroExeSerializer(regs_exe, data = request.data)
        if regs_exe_serializer.is_valid():
            regs_exe_serializer.save()
            return Response({
                'message':'Registro de ejecución actualizado correctamente'
            },status = status.HTTP_200_OK)

        return Response({
            'message':'Hay errores en la actualizaciones de los registros de ejecución',
            'errors':regs_exe_serializer.errors
        },status = status.HTTP_400_BAD_REQUEST)

    # ELIMINA A LOS REGISTROS DE EJECUCIÓN #
    def destroy(self, request, pk=None):
        regs_exe_destroy = self.model.objects.filter(id=pk).update('confirmacion')
        if regs_exe_destroy == 1:
            return Response({
                'message':'Registro de ejecución eliminado correctamente'
            },status = status.HTTP_200_OK)
        return Response({
            'message':'No existe el registro de ejecución que desea eliminar'
        },status = status.HTTP_404_NOT_FOUND)