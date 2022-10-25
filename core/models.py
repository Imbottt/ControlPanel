from email.policy import default
from lib2to3.pytree import Base
from random import choices
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
    """ Modelo para la dirección """
    dir_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.dir_name

### TABLA UNIDAD ###
class Unidad(models.Model):
    """ Modelo para las unidades """
    unidad_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.unidad_name

### TABLA ROL ###
class Rol(models.Model):
    """ Modelo de los roles para los usuarios """
    rol_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.rol_name

### TABLA CARGO ### ---> Funciona como una tabla que alberga sub-roles
class Cargo(models.Model):
    """ Modelo de los cargos para los usuarios """
    cargo_name = models.CharField(max_length=255, unique=True)

### TABLA USUARIO ###
class User(AbstractBaseUser, PermissionsMixin):
    """ Modelo personalizado de Usuario que soporta hacer login con email en vez de usuario """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    ## Llaves foráneas
    rol = models.ForeignKey(Rol, null=True, blank=True, on_delete= models.CASCADE)
    unidad = models.ForeignKey(Unidad, null=True, blank=True, on_delete= models.CASCADE)
    cargo = models.ForeignKey(Cargo, null=True, blank=True, on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'email'

###############################################################################
###############################################################################
###############################################################################

### TABLA FLUJO ###
class Flujo(models.Model):
    """ Modelo para los flujos """
    titulo_flujo = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.titulo_flujo

### TABLA DETALLE-FLUJO ###
class DetalleFlujo(models.Model):
    """ Modelo para el detalle de flujo """
    descripcion_flujo = models.CharField(max_length=255)
    fecha_creacion = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)

    # Llaves foráneas
    flujo_id = models.ForeignKey(Flujo, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion_flujo

### TABLA TAREA ###
class Tarea(models.Model):
    """ Modelo de las tareas """
    titulo_tarea = models.CharField(max_length=30, unique=True)
    descripcion_tarea = models.CharField(max_length=255)
    fecha_creacion = models.DateField(null=True)
    fecha_limite = models.DateField(null=True)
    progreso_tarea = models.CharField(max_length=255)

    detalle_flujo_id = models.ForeignKey(DetalleFlujo, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo_tarea

### TABLA TAREA SUBORDINADA ###
class TareaSubordinada(models.Model):
    """ Modelo para las tareas subordinadas """
    titulo_tarea_sub = models.CharField(max_length=30, unique=True)
    descripcion_tarea_sub = models.CharField(max_length=255)

    # Llaves foráneas
    tarea_id = models.ForeignKey(Tarea, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo_tarea_sub

### TABLA ESTADO TAREA ###
class EstadoTarea(models.Model):
    """ Modelo para los estados de la tarea """
    estado_name = models.CharField(max_length=30, unique=True)
    descripcion_estado = models.CharField(max_length=255)

    def __str__(self):
        return self.estado_name

### TABLA REGISTRO-EJECUCIÓN ###
class RegistroEjecucion(models.Model):
    """ Modelo para el registro de ejecución """
    titulo_registro = models.CharField(max_length=255, unique=True)
    confirmacion = models.BooleanField(null=True)
    justificacion = models.CharField(max_length=255)
    observacion = models.CharField(max_length=255)
    fecha_registro = models.DateField(null=True)

    # Llaves foráneas
    estado_t_id = models.ForeignKey(EstadoTarea, null=True, blank=True, on_delete=models.CASCADE)
    tarea_sub_id = models.ForeignKey(TareaSubordinada, null=True, blank=True, on_delete=models.CASCADE)
    usuario_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo_registro







