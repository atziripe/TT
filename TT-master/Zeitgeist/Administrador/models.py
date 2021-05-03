from django.db import models

class Administrador(models.Model):
    nomUsuario = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=70)
    contrasena = models.CharField(max_length=45)
    correo = models.EmailField()