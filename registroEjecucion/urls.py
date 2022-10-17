from django.urls import path, include
from rest_framework.routers import DefaultRouter

from registroEjecucion import views


router = DefaultRouter()
router.register('CRUD-regExe',views.RolViewSet, basename='CRUD-regExe')

app_name = 'registroEjecucion'

urlpatterns = [
    path('', include(router.urls))
]