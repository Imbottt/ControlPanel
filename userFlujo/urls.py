from django.urls import path, include

from userFlujo import views

app_name = 'userFlujo'

urlpatterns = [
    path('crud-userFlujo/', views.UserFlujoCreateListApiView.as_view(), name='ListCreateUserFlujo'),
    path('crud-userFlujo/<int:pk>/', views.UserFlujoRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyUserFlujo'),
]