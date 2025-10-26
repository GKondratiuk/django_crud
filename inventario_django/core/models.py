# Importación del módulo models de Django para crear modelos de base de datos
from django.db import models
# Importación del modelo User de Django para gestionar usuarios
from django.contrib.auth.models import User

# Definición del modelo Gestoria para almacenar información de gestorías
class Gestoria(models.Model):
    nombre = models.CharField(max_length=100)  # Campo para el nombre de la gestoría, máximo 100 caracteres
    descripcion = models.TextField(blank=True) # Campo de texto opcional para la descripción de la gestoría
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)
    # Clave foránea que relaciona cada gestoría con un usuario responsable
    # on_delete=CASCADE elimina la gestoría si se elimina el usuario

    # Método que define cómo se mostrará el objeto Gestoria como string
    def __str__(self):
        return self.nombre

# Definición del modelo Mueble para gestionar el inventario de muebles
class Mueble(models.Model):
    # Campo para el nombre del mueble, máximo 100 caracteres
    nombre = models.CharField(max_length=100)
    # Campo numérico entero positivo para la cantidad de muebles
    cantidad = models.PositiveIntegerField()
    # Campo opcional para la ubicación del mueble, máximo 100 caracteres
    ubicacion = models.CharField(max_length=100, blank=True)
    # Clave foránea que relaciona cada mueble con una gestoría
    # on_delete=CASCADE elimina los muebles si se elimina la gestoría
    gestoria = models.ForeignKey(Gestoria, on_delete=models.CASCADE)

    # Método que define cómo se mostrará el objeto Mueble como string
    # Retorna el nombre del mueble y su cantidad entre paréntesis
    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"