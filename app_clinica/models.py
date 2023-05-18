from django.db import models
from django.contrib.auth.models import User

# Tabla Raza de los animales
class Raza(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


# Tabla del tipo de animal
class Animal(models.Model):
    nombre = models.CharField(max_length=50)
    raza = models.ForeignKey(Raza, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

# Tabla Categoria (Peluqueria / Operaciones / Consulta Medica)
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Tabla medico veterinario
class Veterinario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

# Tabla peluquera/o
class Peluquera(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre
    
# Tabla de agendamiento
class Agendamiento(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=11)
    correo = models.EmailField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT)
    peluquera = models.ForeignKey(Peluquera, on_delete=models.PROTECT, null=True)
    fecha = models.DateTimeField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
