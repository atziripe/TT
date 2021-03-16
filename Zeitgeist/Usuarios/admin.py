from django.contrib import admin
from Pruebas.models import Paciente
from Especialista.models import Especialista
from Cuidador.models import Cuidador


class PacienteAdmin(admin.ModelAdmin):
    list_display=("nomUsuario", "contraseña")
    search_fields=("nomUsuario","nombre")

class EspecialistaAdmin(admin.ModelAdmin):
    list_display=("nomUsuario", "contraseña")
    search_fields=("nomUsuario","nombre")


class CuidadorAdmin(admin.ModelAdmin):
    list_display=("nomUsuario", "contrasena")
    search_fields=("nomUsuario","nombre")

admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Especialista, EspecialistaAdmin)
admin.site.register(Cuidador, CuidadorAdmin)
