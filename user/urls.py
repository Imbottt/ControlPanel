from django.urls import path 
from user import views

app_name = 'user'

urlpatterns = [
    path('create-user/', views.CreateUserView.as_view(), name='create-user'), #FUNCIONA BIEN
    path('create-token/', views.CreateTokenView.as_view(), name='create-token'), #FUNCIONA BIEN
    path('me/', views.ManageUserView.as_view(), name='me'), #FUNCIONA BIEN
    path('login/', views.Login.as_view(), name='login'), #FUNCIONA BIEN
    path('logout/', views.Logout.as_view(), name='logout') #FUNCIONA
]