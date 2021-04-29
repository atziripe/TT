from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# https://docs.djangoproject.com/en/3.2/ref/contrib/auth/
# class User(models.Model):
#     username -->Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - character
#     first_name
#     last_name
#     email
#     passsword --> SHA256
#     groups --> Many-to-many relationship to Group
#     user_permissions --> Many-to-many relationship to Permission
#     is_staff --> Boolean. Designates whether this user can access the admin site.
#     is_active --> Boolean. Designates whether this user account should be considered active. We recommend that you set this flag to False instead of deleting accounts; that way, if your applications have any foreign keys to users, the foreign keys won’t break.
#     is_superuser -->    Boolean. Designates that this user has all permissions without explicitly assigning them.
#     last_login --> A datetime of the user’s last login.
#     date_joined --> A datetime designating when the account was created. Is set to the current date/time by default when the account is created.

# class OwnerModel(models.Model):
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     class Meta:
#         abstract = True

        
class Especialista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numPacientes = models.IntegerField()
    datos_generales = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.user.username)
 
    class Meta:
        verbose_name_plural = "Especialistas"

class Cuidador(models.Model):
    #id = primary key serial
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return '{}'.format(self.user.username)
 
    class Meta:
        verbose_name_plural = "Cuidadores"

class Administrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.user.username)
 
    class Meta:
        verbose_name_plural = "Administradores"

class Paciente(models.Model):
    ESCOLARIDAD = [
        ('N','Ninguna'),
        ('PR','Primaria'),
        ('SC','Secundaria'),
        ('BCH','Bachillerato'),
        ('SUP','Licenciatura o superior'),
    ]
    GENDER = [
        ('F', "Femenino"),
        ('M', "Masculino"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialista = models.ForeignKey(Especialista, blank=True, null=True, on_delete=models.CASCADE)
    cuidador = models.ForeignKey(Cuidador, blank=True, null=True, on_delete=models.CASCADE)
    escolaridad = models.CharField(choices=ESCOLARIDAD, max_length=50)
    fechaNac = models.DateField()
    sexo = models.CharField(choices=GENDER, max_length=50)
    fechaDiag = models.DateField()

    def __str__(self):
        return '{}'.format(self.user.username)
 
    class Meta:
        verbose_name_plural = "Pacientes"

