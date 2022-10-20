from django.urls import path, include

from rol import views

app_name = 'rol'

urlpatterns = [
    path('crud-rol/', views.RolCreateListApiView.as_view(), name='ListCreateRol'),
    path('crud-rol/<int:pk>/', views.RolRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyRol')
]