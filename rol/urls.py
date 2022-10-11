from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rol import views


router = DefaultRouter()
router.register('create-rol',views.RolViewSet)

app_name = 'rol'

urlpatterns = [
    path('', include(router.urls))
]