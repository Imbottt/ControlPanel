from django.urls import path, include

from notificacion import views

app_name = 'notificacion'

urlpatterns = [
    path('crud-notify/', views.NotifyCreateListApiView.as_view(), name='ListCreateNotificacion'),
    path('crud-notify/<int:pk>/', views.NotifyRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyNotificacion')
]