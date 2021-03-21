from django.contrib import admin
from Pruebas.models import Paciente, Pregunta


class PreguntaAdmin(admin.ModelAdmin):
    list_display=("pregunta", "tipo")
    search_fields=("idReactivo","pregunta")

admin.site.register(Pregunta, PreguntaAdmin)