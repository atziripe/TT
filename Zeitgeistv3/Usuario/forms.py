#Creando clases con API Forms de Django para generar formularios validados
from django import forms

class dateInput (forms.DateInput):
    input_type = 'date'

TYPEU =( 
    ("Administrador", "Administrador"), 
    ("Cuidador", "Cuidador"), 
    ("Especialista", "Especialista"), 
    ("Paciente", "Paciente"), 
)

Escolaridad_enum =(
    ('N','Ninguna'),
    ('PR','Primaria'),
    ('SC','Secundaria'),
    ('BCH','Bachillerato'),
    ('SUP','Licenciatura o superior'),
)

sexo_enum = (
    ('F', "Femenino"),
    ('M', "Masculino"),
)

def dar_estilo_campos(listaCampos): #Brinda el formato apropiado a los campos del formulario
    campos = ['username', 'password', 'nombre','apellidos', 'nombreUsuario', 'correo', 'contrasena', 'confirmacion_cont', 'datos_generales', 'numPacientes','fechaNac', 'fechaDiag']
    for campo in campos:
        try:
        #Asignamos los valores a los campos que si existen en los formularios...
            if(campo == "fechaDiag"):
                listaCampos[campo].widget.attrs.update({'class': 'white-text datepicker', "style": "font-size: 18px;"})
            else:
                listaCampos[campo].widget.attrs.update({'class': 'white-text', "style": "font-size: 18px;"})
        except: #Si no existe, ejecutamos una excepción y nos pasamos al siguiente campo de "campos"
            campo = 'Inexistente'
  
class FormLogin(forms.Form):
    tipo = forms.ChoiceField(choices = TYPEU,label="Iniciarás sesión como ", required=True, widget=forms.Select(attrs={'class': 'browser-default'}))
    username = forms.CharField(label='Nombre de usuario', required=True) 
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)

class FormRegistroC(forms.Form):
    nombre = forms.CharField(label='Nombre:', required=True) 
    apellidos = forms.CharField(label='Apellidos:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.EmailField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirma tu contraseña:', required=True, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)
        

class FormRegistroE(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.EmailField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirma tu contraseña:', required=True, widget=forms.PasswordInput)
    datos_generales = forms.CharField(label='Datos generales:', required=True, widget=forms.Textarea)
    numPacientes = forms.IntegerField(label='Número de pacientes:', required=True, max_value=30, min_value=1,initial=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)
        self.fields['datos_generales'].initial = 'Borra esto y escribe aquí información que consideres importante sobre ti (Unidad Médica, Datos de contacto, etc.)'


class FormRegistroP(forms.Form):
    nombre = forms.CharField(label='Nombre:', required=True) 
    apellidos = forms.CharField(label='Apellidos:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.EmailField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirma tu contraseña:', required=True, widget=forms.PasswordInput)
    sexo = forms.ChoiceField(choices = sexo_enum, label='Género:', required=True, widget=forms.Select(attrs={'class': 'browser-default'}))
    fechaNac = forms.CharField(label='Fecha de Nacimiento:', required=True, widget=dateInput)
    escolaridad = forms.ChoiceField(choices = Escolaridad_enum, label='Escolaridad:', required=True,  widget=forms.Select(attrs={'class': 'browser-default'}))
    fechaDiag = forms.CharField(label='Fecha de Diagnóstico:', required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)


class FormRegistroA(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.EmailField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirma tu contraseña:', required=True, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)

class FormrecuperarPass(forms.Form):
    correo = forms.EmailField(label='Correo electrónico:', required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)