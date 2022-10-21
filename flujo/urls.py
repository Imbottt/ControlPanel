from django.urls import path, include

from flujo import views

app_name = 'flujo'

urlpatterns = [
    path('crud-flujo/', views.FlujoCreateListApiView.as_view(), name='ListCreateFlujo'),
    path('crud-flujo/<int:pk>/', views.FlujoRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyFlujo')
]