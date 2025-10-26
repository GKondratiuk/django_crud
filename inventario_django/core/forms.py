from django import forms
from .models import Gestoria, Mueble

class GestoriaForm(forms.ModelForm):
    class Meta:
        model = Gestoria
        fields = ['nombre', 'descripcion']

class MuebleForm(forms.ModelForm):
    class Meta:
        model = Mueble
        fields = ['nombre', 'cantidad', 'ubicacion']