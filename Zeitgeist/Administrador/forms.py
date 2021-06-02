#Creando clases con API Forms de Django para generar formularios validados
from django import forms
from Pruebas.forms import dar_estilo_campos 



class FormEditarA(forms.Form):
    nvo_nombre = forms.CharField(label='Nuevo nombre (completo):', required=True, widget=forms.Textarea) 
    nvo_nombreUsuario = forms.CharField(label='Nuevo nombre de usuario:', required=True) 
    nvo_correo = forms.CharField(label='Nuevo correo electrónico:', required=True)  
    nvo_contrasena = forms.CharField(label='Nueva contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Contraseña actual:', required=True, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)

class FormModificarRelacion(forms.Form):
    paciente = forms.CharField(label='Paciente a modificar:', required=True, widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)
        
class FormEliminarPerfil(forms.Form):
    perfil = forms.CharField(label='Usuario a eliminar:', required=True, widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)