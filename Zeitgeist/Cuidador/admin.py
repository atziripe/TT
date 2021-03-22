from django.contrib import admin
from .models import Cat_Pregunta, Pregunta


class PreguntaAdmin(admin.ModelAdmin):
    list_display=("idReactivo", "respuestaCuidador")
    search_fields=("idReactivo","respuestaCuidador")

class CatPreguntaAdmin(admin.ModelAdmin):
    list_display=("reactivo", "tipoDato")
    search_fields=("idReactivo","reactivo")

admin.site.register(Cat_Pregunta, CatPreguntaAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
