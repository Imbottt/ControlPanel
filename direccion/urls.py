from django.urls import path, include

from direccion import views

app_name = 'direccion'

urlpatterns = [
    path('crud-dir/', views.DirListCreateApiView.as_view(), name='ListCreateDir'),
    path('crud-dir/<int:pk>/', views.DirRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyDir')
]