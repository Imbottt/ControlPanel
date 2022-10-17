from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tarea import views


router = DefaultRouter()
router.register('CRUD-tarea',views.TareaViewSet, basename='CRUD-tarea')

app_name = 'tarea'

urlpatterns = [
    path('', include(router.urls))
]