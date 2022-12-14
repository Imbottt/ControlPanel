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

        user = self.model(email=self.normalize_email(email), **extra_fields)
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
    unidad_name = models.CharField(max_length=255,null=True, unique=True)

    # Claves foráneas
    dir = models.ForeignKey(Direccion, null=True, on_delete=models.CASCADE) # SI SE BORRA LA DIRECCIÓN, LA UNIDAD TAMBIÉN DESAPARECERÁ

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
    rol = models.ForeignKey(Rol, null=True, on_delete=models.CASCADE) # SI SE BORRA EL ROL, EL USUARIO PERMANECE
    cargo = models.ForeignKey(Cargo, null=True, on_delete=models.CASCADE) # SI SE BORRA EL CARGO, EL USUARIO PERMANECE
    unidad = models.ForeignKey(Unidad, null=True, on_delete=models.CASCADE) # SI SE BORRA LA UNIDAD, EL USUARIO PERMANECE

    objects = UserManager()

    USERNAME_FIELD = 'email'

###############################################################################
###############################################################################
###############################################################################

### TABLA FLUJO ###
class Flujo(models.Model):
    """ Tabla para los flujos """

    flujo_choices = (
        ("Seleccionar", "1"),
        ("Ejecutando", "2"),
        ("Sin ejecutar", "3")
    )

    flujo_name = models.CharField(max_length=50, unique=True)
    descripcion_flujo = models.CharField(max_length=255)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateField(auto_now=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    plazo_flujo = models.CharField(max_length=50)
    creador_flujo = models.PositiveIntegerField()
    ejecutar = models.CharField(max_length=10, choices=flujo_choices)

    # Fecha de ahora
    @property
    def fecha_actual(self):
        fecha_ahora = datetime.now().date()
        return fecha_ahora
    
    # Plazo
    @property
    def get_plazo_f(self):
        fecha_fin = self.fecha_fin
        fecha_inicio = self.fecha_inicio
        plazo = fecha_fin - fecha_inicio
        return plazo.days

    # Cálculo % de avances

    def save(self, *args, **kwargs):
        self.plazo_flujo = self.get_plazo_f
        super(Flujo, self).save(*args, **kwargs)

    def __str__(self):
        return self.flujo_name

### TABLA TAREA ###
class Tarea(models.Model):
    """ Tabla de las tareas """
    #id_tarea = models.AutoField(primary_key=True, unique=True)
    titulo_tarea = models.CharField(max_length=50, unique=True)
    descripcion_tarea = models.CharField(max_length=255)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_limite = models.DateField()  
    plazo_tarea = models.CharField(max_length=255)
    progreso_tarea = models.CharField(max_length=255)
    creador_tarea = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo_tarea

    # PROGRESO
    @property
    def get_fecha_hoy(self):
        return datetime.now().date()

    @property
    def get_progreso(self):
        return self.get_fecha_fin - self.get_fecha_hoy

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
        self.plazo_tarea = self.get_plazo
        self.progreso_tarea = self.get_progreso
        super(Tarea, self).save(*args, **kwargs)

### TABLA USER - TAREA ###
class UserTarea(models.Model):
    """ Tabla de usuario - tarea """

    estado_choices = (
    ("0","Sin asignar"),
    ("1","Por empezar"), 
    ("2", "En progreso"), 
    ("3","Finalizada"),
    ####################
    ("4","Aceptada"),
    ("5","Rechazada"),
    ) 

    #id_userTarea = models.AutoField(primary_key=True)
    asignador = models.PositiveIntegerField() # Usuario que asignó la tarea

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

### TABLA REPORTE ###
class Reporte(models.Model):
    """ Tabla de Alertas """

    id_reportador_rechazador = models.PositiveIntegerField()
    justificacion = models.CharField(max_length=255)
    is_reported = models.BooleanField(default=False)
    # Claves foráneas
    tarea = models.ForeignKey(Tarea, null=True, on_delete=models.CASCADE)
    asignador_tarea = models.PositiveIntegerField()

    def __str__(self):
        return self.justificacion

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
    #id_regExe = models.AutoField(primary_key=True)
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

### TABLA NOTIFICACIÓN ###
class Notificacion(models.Model):
    """ Tabla para las notificaciones """
    id_notificador = models.PositiveIntegerField()
    id_notificado = models.PositiveIntegerField()
    mensaje = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    # Clave foránea
    tarea = models.ForeignKey(Tarea, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.is_read)

### TABLA TAREA RELACIONADA ###
class TareaRelacionada(models.Model):
    """ Tabla para las tareas relacionadas """
    id_tarea_main = models.PositiveIntegerField(null=True)
    id_tarea_relational = models.PositiveIntegerField(null=True)

    def __str__(self):
        return str(self.id_tarea_main)

### TABLA USER - TAREA - TAREA SUBORDINADA ###
class UserTSubTarea(models.Model):
    """ Tabla para las tareas asociadas a usuarios y tareas subordinadas """

    id_padre = models.PositiveIntegerField()
    asignador = models.PositiveIntegerField()

    # Clave foránea
    userTarea = models.ForeignKey(UserTarea, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_padre)


