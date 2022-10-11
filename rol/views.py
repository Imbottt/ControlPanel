from importlib.util import resolve_name
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Roll

from rol import serializers

###
from rest_framework.response import Response
from rest_framework import status
###

class RolViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """ Manejar los roles en la BD """
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RolSerializer
    queryset = Roll.objects.all()

    def get_queryset(self):
        """ Retornar objetos para el usuario autentificado """
        return self.queryset.filter(user=self.request.user)

    ## CREAR ROL ##
    def perform_create(self, serializer):
        """ Crear nuevo rol """
        serializer.save(user=self.request.user)


    

    

    



