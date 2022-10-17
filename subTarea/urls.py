from django.urls import path, include
from rest_framework.routers import DefaultRouter

from subTarea import views


router = DefaultRouter()
router.register('CRUD-subtarea',views.SubTareaViewSet, basename='CRUD-subtarea')

app_name = 'subTarea'

urlpatterns = [
    path('', include(router.urls))
]