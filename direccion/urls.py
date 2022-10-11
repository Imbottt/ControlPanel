from django.urls import path, include
from rest_framework.routers import DefaultRouter

from direccion import views


router = DefaultRouter()
router.register('create-dir',views.DirViewSet)

app_name = 'direccion'

urlpatterns = [
    path('', include(router.urls))
]