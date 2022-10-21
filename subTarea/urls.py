from django.urls import path, include

from subTarea import views

app_name = 'subTarea'

urlpatterns = [
    path('crud-subTarea/', views.SubTareaCreateListApiView.as_view(), name='ListCreateSubTarea'),
    path('crud-subTarea/<int:pk>/', views.SubTareaRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroySubTarea')
]