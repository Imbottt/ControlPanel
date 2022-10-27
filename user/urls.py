from django.urls import path, include 
from user import views

app_name = 'user'

### URLS  ### 
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'), #FUNCIONA
    path('logout/', views.Logout.as_view(), name='logout'), #FUNCIONA
    path('create-superuser/', views.CreateSuperUserView.as_view(), name='create-superuser'), #FUNCIONA
    path('crud-user/', views.UserCreateListApiView.as_view(), name='list-create-user'),
    path('crud-user/<int:pk>/', views.UserRetrieveUpdateDestroyApiView.as_view(), name='retrieve-update-destroy-user')
]