from django.contrib import admin
from Pruebas.models import Paciente
from Especialista.models import Especialista
from Cuidador.models import Cuidador
from Administrador.models import Administrador


<<<<<<< HEAD
# class PacienteAdmin(admin.ModelAdmin):
#     list_display=("nomUsuario", "contrasena")
#     search_fields=("nomUsuario","nombre")
=======
class PacienteAdmin(admin.ModelAdmin):
    list_display=("nomUsuario", "contraseña")
    search_fields=("nomUsuario","nombre")
>>>>>>> 1f8d1b344bf99061a0bdae79ab6b28bc118e9111

class EspecialistaAdmin(admin.ModelAdmin):
    list_display=("nomUsuario", "contrasena")
    search_fields=("nomUsuario","nombre")


class CuidadorAdmin(admin.ModelAdmin):
    list_display=("nomUsuario", "contrasena")
    search_fields=("nomUsuario","nombre")

<<<<<<< HEAD
# admin.site.register(Paciente, PacienteAdmin)
=======
class AdministradorAdmin(admin.ModelAdmin):
    list_display=("nomUsuario", "contrasena")
    search_fields=("nomUsuario","nombre")

admin.site.register(Paciente, PacienteAdmin)
>>>>>>> 1f8d1b344bf99061a0bdae79ab6b28bc118e9111
admin.site.register(Especialista, EspecialistaAdmin)
admin.site.register(Cuidador, CuidadorAdmin)
admin.site.register(Administrador, AdministradorAdmin)
