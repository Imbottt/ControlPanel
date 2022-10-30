from django.urls import path, include

from cargo import views

app_name = 'cargo'

urlpatterns = [
    path('crud-cargo/', views.CargoCreateListApiView.as_view(), name='ListCreateCargo'),
    path('crud-cargo/<int:pk>/', views.CargoRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyCargo')
]