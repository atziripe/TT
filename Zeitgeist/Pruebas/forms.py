from django import forms

  
class FormReactivosARem(forms.Form):
    cveaccess = forms.CharField(widget=forms.HiddenInput())
    idReactivo = forms.CharField(widget=forms.HiddenInput())
    respuesta = forms.CharField(label="Tu respuesta", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'input-field'}))

class FormReactivosOPRem(forms.Form):
    cveaccess = forms.CharField(widget=forms.HiddenInput())
    idReactivo = forms.CharField(widget=forms.HiddenInput())
    respuesta = forms.CharField(label="Tu respuesta", max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'input-field'}))


    