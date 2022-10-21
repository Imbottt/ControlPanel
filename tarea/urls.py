from django.urls import path, include

from tarea import views

app_name = 'tarea'

urlpatterns = [
    path('crud-tarea/', views.TareaCreateListApiView.as_view(), name='ListCreateTarea'),
    path('crud-tarea/<int:pk>/', views.TareaRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyTarea')
]