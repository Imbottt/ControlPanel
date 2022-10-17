from django.urls import path, include
from rest_framework.routers import DefaultRouter

from unidad import views


router = DefaultRouter()
router.register('CRUD-unidad',views.UnidadViewSet, basename='CRUD-unidad')

app_name = 'unidad'

urlpatterns = [
    path('', include(router.urls))
]