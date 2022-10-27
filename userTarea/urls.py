from django.urls import path, include

from userTarea import views

app_name = 'userTarea'

urlpatterns = [
    path('crud-userTarea/', views.UserTareaCreateListApiView.as_view(), name='ListCreateUserTarea'),
    path('crud-userTarea/<int:pk>/', views.UserTareaRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyUserTarea'),
]