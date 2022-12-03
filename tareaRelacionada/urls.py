from django.urls import path, include

from tareaRelacionada import views

app_name = 'tareaRelacionada'

urlpatterns = [
    path('crud-tareaRel/', views.TareaRelCreateListApiView.as_view(), name='ListCreateTareaRelacional'),
    path('crud-tareaRel/<int:pk>/', views.TareaRelRetrieveUpdateDestroyApiView.as_view(), name='RetrieveUpdateDestroyTareaRelacional')
]