from importlib.util import resolve_name
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Direccion

from direccion import serializers

###
from rest_framework.response import Response
from rest_framework import status
###

class DirViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """ Manejar las direcciones en la BD """
    serializer_class = serializers.DirSerializer
    queryset = Direccion.objects.all()

    