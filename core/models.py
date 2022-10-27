from datetime import datetime
from email.policy import default
from lib2to3.pytree import Base
from random import choices
from secrets import choice
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from xml.etree.ElementInclude import default_loader
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings


##### MANAGER DEL USUARIO #####
class UserManager(BaseUserManager):

    ## USUARIO NORMAL
    def create_user(self, email, password=None, **extra_fields):
        """ Crear y guardar un nuevo usuario """
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    ## SUPER USUARIO
    def create_superuser(self, email, password, **extra_fields):
        """ Crear super usuario """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

###############################################################################
############################### MODELO DE LA BD ###############################
###############################################################################

### TABLA DIRECCIÓN ###
class Direccion(models.Model):
    """ Tabla para las direcciones """
    dir_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.dir_name

### TABLA UNIDAD ###
class Unidad(models.Model):
    """ Tabla para las unidades """
    unidad_name = models.CharField(max_length=255, unique=True)

    # Claves foráneas
    dir = models.ForeignKey(Direccion, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.unidad_name

### TABLA ROL ###
class Rol(models.Model):
    """ Tabla para los roles """
    rol_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.rol_name

### TABLA CARGO ### ---> Funciona como una tabla que alberga sub-roles
class Cargo(models.Model):
    """ Tabla para los cargos """
    cargo_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.cargo_name

### TABLA USUARIO ###
class User(AbstractBaseUser, PermissionsMixin):
    """ Modelo personalizado de Usuario que soporta hacer login con email en vez de usuario """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    creador = models.IntegerField(default=0)

    ## Claves foráneas
    rol = models.ForeignKey(Rol, null=True, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, null=True, on_delete=models.CASCADE)
    unidad = models.ForeignKey(Unidad, null=True, on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'email'

###############################################################################
###############################################################################
###############################################################################

### TABLA FLUJO ###
class Flujo(models.Model):
    """ Tabla para los flujos """
    flujo_name = models.CharField(max_length=50, unique=True)
    descripcion_flujo = models.CharField(max_length=255)
    fecha_creacion = models.DateField(null=True)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)

    # Clave foránea
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.flujo_name

### TABLA ESTADO TAREA ###
class EstadoTarea(models.Model):
    """ Modelo para los estados de la tarea """
    estado_name = models.CharField(max_length=30, unique=True)
    descripcion_estado = models.CharField(max_length=255)

    def __str__(self):
        return self.estado_name

### TABLA TAREA ###
class Tarea(models.Model):
    """ Tabla de las tareas """
    titulo_tarea = models.CharField(max_length=50, unique=True)
    descripcion_tarea = models.CharField(max_length=255)
    fecha_creacion = datetime.now()
    fecha_inicio = models.DateField(null=True)
    fecha_limite = models.DateField(null=True)
    progreso_tarea = models.CharField(max_length=255)
    # Claves foráneas
    estado = models.ForeignKey(EstadoTarea, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.titulo_tarea

### TABLA USER - TAREA ###
class UserTarea(models.Model):
    """ Tabla de flujo - tarea """
    asignacion = models.CharField(max_length=255, unique=True)
    # Claves foráneas
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.asignacion

### TABLA ALERTA ###
alerta_choices = (
    ("0", "--------"), 
    ("1", "Acepto"), 
    ("2", "Rechazo"), 
) 

class Alertas(models.Model):
    """ Tabla de Alertas """
    confirmacion = models.CharField(max_length=10, choices=alerta_choices, default=0)
    justificacion = models.CharField(max_length=255)

    # Claves foráneas
    tarea = models.ForeignKey(Tarea, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.id, self.confirmacion

### TABLA TAREA SUBORDINADA ###
class TareaSubordinada(models.Model):
    """ Tabla para las tareas subordinadas """
    titulo_subTarea = models.CharField(max_length=30, unique=True)
    descripcion_subTarea = models.CharField(max_length=255)
    fecha_creacion = models.DateField(null=True)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)

    # Llaves foráneas
    tarea = models.ForeignKey(Tarea, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo_subTarea

### TABLA REGISTRO-EJECUCIÓN ###
class RegistroEjecucion(models.Model):
    """ Tabla para el registro de ejecución """
    titulo_reg = models.CharField(max_length=255, unique=True)
    fecha_reg = models.DateField(null=True)

    # Claves foráneas
    userTarea = models.ForeignKey(UserTarea, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo_reg








