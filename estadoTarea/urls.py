from django.urls import path, include

from estadoTarea import views

app_name = 'estadoTarea'

urlpatterns = [
    path('crud-estado-tarea/', views.EstadoTareaCreateListApiView.as_view(), name='ListCreateEstadoTarea'),
    path('crud-estado-tarea/<int:pk>/', views.EstadoTareaRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyEstadoTarea'),
]