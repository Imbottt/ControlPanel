from django.urls import path, include

from unidad import views

app_name = 'unidad'

urlpatterns = [
    path('crud-unidad/', views.UnidadCreateListApiView.as_view(), name='ListCreateUnidad'),
    path('crud-unidad/<int:pk>/', views.UnidadRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyUnidad'),
]