from django.db import models


class Usuario(models.Model):
    nomUsuario = models.CharField(primary_key = True, max_length=20)
    nombre = models.CharField(max_length=70)
    contraseña = models.CharField(max_length=45)
    correo = models.EmailField()
    tipo = models.CharField(max_length=1)
