from django import forms

  
class FormAccederRem(forms.Form):
    cveaccess = forms.CharField(label='Clave de acceso', required=True) 


    