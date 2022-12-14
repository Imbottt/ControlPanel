"""TaskControl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/cargo/', include('cargo.urls')),
    path('api/rol/', include('rol.urls')),
    path('api/dir/', include('direccion.urls')),
    path('api/unidad/', include('unidad.urls')),
    path('api/tarea/', include('tarea.urls')),
    path('api/subTarea/', include('subTarea.urls')),
    path('api/flujo/', include('flujo.urls')),
    path('api/reporte/', include('reporte.urls')),
    path('api/userTarea/', include('userTarea.urls')),
    path('api/userFlujo/', include('userFlujo.urls')),
    path('api/notificacion/', include('notificacion.urls')),
    path('api/registroEjecucion/', include('registroEjecucion.urls')),
    path('api/registroFlujo/', include('registroFlujo.urls')),
    path('api/tareaRel/', include('tareaRelacionada.urls')),
    path('api/UserTSubTarea/', include('UserTSubTarea.urls')),
    #
]
