from django.urls import path, include

from registroEjecucion import views

app_name = 'registroEjecucion'

urlpatterns = [
    path('crud-regExe/', views.RegistroExeCreateListApiView.as_view(), name='ListCreateRegistroExe'),
    path('crud-regExe/<int:pk>/', views.RegistroExeRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyRegistroExe')
]