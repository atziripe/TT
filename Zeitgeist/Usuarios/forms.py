#Creando clases con API Forms de Django para generar formularios validados
from django import forms

class dateInput (forms.DateInput):
    input_type = 'date'

TYPEU =( 
    ("1", "Administrador"), 
    ("2", "Cuidador"), 
    ("3", "Especialista"), 
    ("4", "Paciente"), 
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
    campos = ['username', 'password', 'nombre', 'nombreUsuario', 'correo', 'contrasena', 'confirmacion_cont', 'datos_generales', 'numPacientes','fechaNac', 'fechaDiag']
    for campo in campos:
        try:
        #Asignamos los valores a los campos que si existen en los formularios...
            listaCampos[campo].widget.attrs.update({'class': 'white-text', "style": "font-size: 18px;"})
        except: #Si no existe, ejecutamos una excepción y nos pasamos al siguiente campo de "campos"
            campo = 'Inexistente'
  
class FormLogin(forms.Form):
    tipo = forms.ChoiceField(choices = TYPEU,label="Usted iniciará sesión como ", required=True, widget=forms.Select(attrs={'class': 'browser-default'}))
    username = forms.CharField(label='Nombre de usuario', required=True) 
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)

class FormRegistroC(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.CharField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirme su contraseña:', required=True, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)
        

class FormRegistroE(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario (cédula profesional de especialista):', required=True) 
    correo = forms.CharField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirme su contraseña:', required=True, widget=forms.PasswordInput)
    datos_generales = forms.CharField(label='Datos generales:', required=True, widget=forms.Textarea(attrs={'placeholder':'Escriba aquí la información (datos de contacto, especialización, domicilio de consultorio, etc).'}))
    numPacientes = forms.IntegerField(label='Número de pacientes:', required=True, max_value=30, min_value=1,initial=1)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)
        self.fields['datos_generales'].widget.attrs['style']  = 'width:100%; height: 80px; background-color: #333;'


class FormRegistroP(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.CharField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirme su contraseña:', required=True, widget=forms.PasswordInput)
    sexo = forms.ChoiceField(choices = sexo_enum, label='Género:', required=True, widget=forms.Select(attrs={'class': 'browser-default'}))
    fechaNac = forms.DateField(label='Fecha de Nacimiento:', required=True, widget=dateInput)
    escolaridad = forms.ChoiceField(choices = Escolaridad_enum, label='Escolaridad:', required=True,  widget=forms.Select(attrs={'class': 'browser-default'}))
    fechaDiag = forms.DateField(label='Fecha de Diagnóstico:', required=True,  widget=dateInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)


class FormRegistroA(forms.Form):
    nombre = forms.CharField(label='Nombre completo:', required=True) 
    nombreUsuario = forms.CharField(label='Nombre de usuario:', required=True) 
    correo = forms.CharField(label='Correo Electrónico:', required=True)  
    contrasena = forms.CharField(label='Contraseña:', required=True, widget=forms.PasswordInput)
    confirmacion_cont = forms.CharField(label='Confirme su contraseña:', required=True, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)

class FormrecuperarPass(forms.Form):
    correo = forms.EmailField(label='Correo electrónico:', required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dar_estilo_campos(self.fields)
    