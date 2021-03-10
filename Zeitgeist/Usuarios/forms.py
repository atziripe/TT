#Creando clases con API Forms de Django para generar formularios validados
from django import forms


TYPEU =( 
    ("1", "Administrador"), 
    ("2", "Cuidador"), 
    ("3", "Especialista"), 
    ("4", "Paciente"), 
) 
  
class FormLogin(forms.Form):
    tipo = forms.ChoiceField(choices = TYPEU,label="Usted está ingresando como ", required=True, widget=forms.Select(attrs={'class': 'browser-default'}))
    username = forms.CharField(label='Nombre de usuario', required=True) 
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput)

    
