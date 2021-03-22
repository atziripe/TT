from django import forms

class IngresoDatosT(forms.Form):
   respuesta = forms.CharField(required=True)


class FormDatosImg(forms.Form):
    respuesta = forms.CharField(required=True)
    imagen = forms.ImageField(required=True)