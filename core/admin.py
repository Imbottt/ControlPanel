from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email','name']
    fieldsets = (
        (None,{'fields': ('email','password')}),
        (_('Personal Info'),{'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields':('is_active','is_staff','is_superuser')}
            ),
        (_('Important Dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }),
    )

## MODELOS QUE SE REGISTRAROM EN ADMIN
admin.site.register(models.User, UserAdmin) # -Tabla Usuario
admin.site.register(models.Rol) # Tabla Rol
admin.site.register(models.Direccion) # Tabla Dirección
admin.site.register(models.Unidad) # Tabla Unidad
admin.site.register(models.UserTarea) # Tabla User - Tarea
admin.site.register(models.Flujo) # Tabla Flujo
admin.site.register(models.Tarea) # Tabla Tarea
admin.site.register(models.TareaSubordinada) # Tabla Tarea Subordinada
admin.site.register(models.RegistroEjecucion) # Tabla Dirección
admin.site.register(models.Cargo) # Tabla Cargo
admin.site.register(models.Alertas) # Tabla Alerta
admin.site.register(models.RegistroFlujo)# Tabla Registro Flujos
admin.site.register(models.Notificacion)# Tabla Notificacion
admin.site.register(models.TareaRelacionada)# Tabla Tarea Relacionada
