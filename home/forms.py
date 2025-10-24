#forms.py fue creada de manera manual para crear y gestionar inventarios 
from django.forms import ModelForm #importa modelos de formularios
from .models import Objeto #el modelo que creamos en en models.py

class elementos_formulario(ModelForm):
    class Meta:
        model = Objeto #importamos el model oque creamos
        fields = ['title','description']