from django.contrib import admin
from .models import Tema, Palabra, Ent_Cogn

class TemaAdmin(admin.ModelAdmin):
    list_display=("cveTemas","tema","dificultad",)

class PalabraAdmin(admin.ModelAdmin):
    list_display=("cvePalabra","tema","palabra",)

class EntCognAdmin(admin.ModelAdmin):
    list_display=("cveAcceso","cveTema","paciente","fechaAp","estado","tiempo")

admin.site.register(Tema, TemaAdmin)
admin.site.register(Palabra, PalabraAdmin)
admin.site.register(Ent_Cogn, EntCognAdmin)