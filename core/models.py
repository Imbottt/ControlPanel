from datetime import datetime
from email.policy import default
from lib2to3.pytree import Base, convert
from random import choices
from secrets import choice
from time import strftime
from tkinter import CASCADE, ROUND
from unittest.util import _MAX_LENGTH
from xml.etree.ElementInclude import default_loader
from xmlrpc.client import _datetime_type
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.settings import api_settings

from django.conf import settings
from django.forms import DateField


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
    dir = models.ForeignKey(Direccion, null=True, on_delete=models.DO_NOTHING) # SI SE BORRA LA DIRECCIÓN, LA UNIDAD PERMANECE

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
    rol = models.ForeignKey(Rol, null=True, on_delete=models.DO_NOTHING) # SI SE BORRA EL ROL, EL USUARIO PERMANECE
    cargo = models.ForeignKey(Cargo, null=True, on_delete=models.DO_NOTHING) # SI SE BORRA EL CARGO, EL USUARIO PERMANECE
    unidad = models.ForeignKey(Unidad, null=True, on_delete=models.DO_NOTHING) # SI SE BORRA LA UNIDAD, EL USUARIO PERMANECE

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
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    plazo_flujo = models.CharField(max_length=255)
    progreso_f = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    @property
    def get_fecha_hoy(self):
        return datetime.now()

    @property
    def get_fecha_fin(self):
        f_fin = self.fecha_fin
        return f_fin

    @property
    def get_plazo_flujo(self):
        plazo_f = self.get_fecha_fin.replace(tzinfo=None) - self.get_fecha_hoy
        return plazo_f

    @property
    def get_progeso_flujo(self):
        progreso_f = self.fecha_inicio - self.get_plazo_flujo

    def save(self, *args, **kwargs):
        self.plazo_flujo = self.get_plazo_flujo
        self.progreso_f = self.get_progeso_flujo
        super(Flujo, self).save(*args, **kwargs)

    def __str__(self):
        return self.flujo_name

### TABLA TAREA ###
class Tarea(models.Model):
    """ Tabla de las tareas """
    titulo_tarea = models.CharField(max_length=50, unique=True)
    descripcion_tarea = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_inicio = models.DateTimeField(null=True)
    fecha_limite = models.DateTimeField(null=True) 
    plazo_tarea = models.CharField(max_length=255)
    progreso_tarea = models.CharField(max_length=255)
    creador_tarea = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo_tarea

    # PROGRESO
    @property
    def get_fecha_hoy(self):
        return datetime.now()

    @property
    def get_progreso(self):
        return self.get_fecha_fin.replace(tzinfo=None) - self.get_fecha_hoy

    ## PLAZO
    @property
    def get_fecha_ini(self):
        return self.fecha_inicio

    @property
    def get_fecha_fin(self):
        return self.fecha_limite

    @property
    def get_plazo(self):
        return (self.get_fecha_fin - self.get_fecha_ini)

    def save(self, *args, **kwargs):
        self.fecha_inicio = self.get_fecha_ini
        self.fecha_limite = self.get_fecha_fin
        self.plazo_tarea = self.get_plazo
        self.progreso_tarea = self.get_progreso
        super(Tarea, self).save(*args, **kwargs)

### TABLA USER - TAREA ###
class UserTarea(models.Model):
    """ Tabla de flujo - tarea """

    estado_choices = (
    ("Sin asignar", "1"), 
    ("En progreso", "2"), 
    ("Finalizada", "3"),
    ) 

    asignador = models.IntegerField() # Usuario que asignó la tarea

    # Claves foráneas
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) # SI SE BORRA EL USUARIO, LA ASIGNACIÓN TAMBIÉN SE BORRARÁ
    tarea = models.ForeignKey(Tarea, null=True, on_delete=models.CASCADE) # SI SE BORRA LA TAREA, LA ASIGNACIÓN TAMBIÉN SE BORRARÁ
    estado_tarea = models.CharField(max_length=12, choices=estado_choices, default=None)

    def __str__(self):
        return str(self.asignador)

### TABLA USER - FLUJO ###
class UserFlujo(models.Model):
    """ Tabla de flujo - tarea """
    asignador = models.IntegerField() # Usuario que asignó el flujo

    # Claves foráneas
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) # SI SE BORRA EL USUARIO, LA ASIGNACIÓN TAMBIEN SE BORRARÁ
    flujo = models.ForeignKey(Flujo, null=True, on_delete=models.CASCADE) # SI SE BORRA EL USUARIO, LA ASIGNACIÓN TAMBIÉN SE BORRARÁ

    def __str__(self):
        return str(self.asignador)

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
        return self.confirmacion

### TABLA TAREA SUBORDINADA ###
class TareaSubordinada(models.Model):
    """ Tabla para las tareas subordinadas """
    titulo_subTarea = models.CharField(max_length=30, unique=True)
    descripcion_subTarea = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)

    # Llaves foráneas
    tarea = models.ForeignKey(Tarea, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo_subTarea

### TABLA REGISTRO-EJECUCIÓN ###
class RegistroEjecucion(models.Model):
    """ Tabla para el registro de ejecución """
    titulo_reg = models.CharField(max_length=255, unique=True)
    fecha_reg = models.DateTimeField(auto_now_add=True, null=True)

    # Claves foráneas
    userTarea = models.ForeignKey(UserTarea, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo_reg

### TABLA REGISTRO-FLUJOS ###
class RegistroFlujo(models.Model):
    """ Tabla para el registro de flujos """
    titulo_reg_f = models.CharField(max_length=255, unique=True)
    fecha_reg = models.DateTimeField(auto_now_add=True)

    # Llave foránea
    userFlujo = models.ForeignKey(UserFlujo, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo_reg_f







