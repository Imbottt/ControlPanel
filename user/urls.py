from django.urls import path, include 
from user import views

from rest_framework.routers import DefaultRouter

app_name = 'user'

router = DefaultRouter()
router.register('Crud-User',views.UserViewSet, basename='CRUD-user')

### URLS  ### 
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'), #FUNCIONA
    path('logout/', views.Logout.as_view(), name='logout'), #FUNCIONA
    path('create-superuser/', views.CreateSuperUserView.as_view(), name='create-superuser'), #FUNCIONA

    ### URLS PARA LOS ROUTERS ###
    path('', include(router.urls)),
]