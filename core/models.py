from email.policy import default
from lib2to3.pytree import Base
from random import choices
from tkinter import CASCADE
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
    def create_superuser(self, email, password):
        """ Crear super usuario """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

### TABLA ROL ###
class Roll(models.Model):
    """ Modelo de los roles para los usuarios """
    rol_name = models.CharField(max_length=25)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.rol_name

### TABLA DIRECCIÓN ###
class Direccion(models.Model):
    """ Modelo para la dirección """
    dir_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.dir_name

### TABLA UNIDAD ###

### TABLA USUARIO ###
class User(AbstractBaseUser, PermissionsMixin):
    """ Modelo personalizado de Usuario que soporta hacer login con email en vez de usuario """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    rol = models.ForeignKey(Roll, blank=True, null=True, on_delete=models.CASCADE)
    dir_user = models.ForeignKey(Direccion, blank=True, null=True, on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'email'



### TABLA ESTADO-TAREA ###
### TABLA TAREA ###
### TABLA TAREA SUBORDINADA ###
### TABLA FLUJO ###
### TABLA DETALLE-FLUJO ###
### TABLA REGISTRO-EJECUCIÓN ###



