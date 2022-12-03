from django.urls import path, include

from reporte import views

app_name = 'reporte'

urlpatterns = [
    path('crud-reporte/', views.ReporteCreateListApiView.as_view(), name='ListCreateReporte'),
    path('crud-reporte/<int:pk>/', views.ReporteRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyReporte')
]