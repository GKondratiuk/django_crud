from django.db import models
from django.contrib.auth.models import User
# Create your models here. los modelos son para interactuar con la base de datos

class Objeto(models.Model): #crea nuestra tabla a lo sql 
    title = models.CharField(max_length=100) #agrega texto corto
    description = models.TextField(blank = True) #agrega texto amplio
    created = models.DateTimeField(auto_now_add=True) #agrega la fecha en que fue creado de manera automatica
    user = models.ForeignKey(User, on_delete = models.CASCADE) #relacionamos al objeto cargado con el usuario

    def __str__(self):
        return f"{self.title} - creado por: {self.user.username} - fecha: {self.created.strftime('%Y-%m-%d %H:%M')}"

#DESPUES DE CREAR LOS MODELOS HAY QUE HACER UN PYTHON3 MANAGE.PY MAKEMIGRATIONS
#DESPUES MIGRARLOS - PYTHON3 MANAGE.PY MIGRATE