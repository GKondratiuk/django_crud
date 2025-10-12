from django.contrib import admin
from .models import Objeto

class ObjetoAdmin(admin.ModelAdmin): #creamos objeto de solo lectura que muestre cuando se creó la tarea
    readonly_fields = ("created", )

# Register your models here. esta seccion sirve para agregar las tablas que realizamos a la seccion del administrador
admin.site.register(Objeto, ObjetoAdmin) #agregamos el objeto que creamos en la seccion de models.py