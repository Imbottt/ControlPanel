from django.urls import path, include

from alerta import views

app_name = 'alerta'

urlpatterns = [
    path('crud-alerta/', views.AlertaCreateListApiView.as_view(), name='ListCreateAlerta'),
    path('crud-alerta/<int:pk>/', views.AlertaRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyAlerta')
]