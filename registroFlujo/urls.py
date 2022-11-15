from django.urls import path, include

from registroFlujo import views

app_name = 'registroFlujo'

urlpatterns = [
    path('crud-regFlu/', views.RegFluCreateListApiView.as_view(), name='ListCreateRegistroFlujo'),
    path('crud-regFlu/<int:pk>/', views.RegFluRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyRegistroFlujo')
]