from django.urls import path, include

from UserTSubTarea import views

app_name = 'UserTSubTarea'

urlpatterns = [
    path('crud-UserTSubTarea/', views.UserTSubTareaCreateListApiView.as_view(), name='ListCreateUserTSubTarea'),
    path('crud-UserTSubTarea/<int:pk>/', views.UserTSubTareaRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyUserTSubTarea')
]