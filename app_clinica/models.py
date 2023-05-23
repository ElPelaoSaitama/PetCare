from django.db import models
from django.contrib.auth.models import User

# test para agendamiento
from datetime import date
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ForeignKey
import locale
from django.db.models.fields.related import ForeignKey, OneToOneField


# Tabla del tipo de animal
class Especie(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Tabla Raza de los animales
class Raza(models.Model):
    nombre = models.CharField(max_length=50)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)

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
    
# Tabla Contacto
class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    asunto = models.CharField(max_length=50)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre

# Tabla para los clientes
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nac = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.user.username

# Tabla para las mascotas
class Mascota(models.Model):
    dueno = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    raza = models.ForeignKey(Raza, on_delete=models.CASCADE)

    sexo_choices = (
        ("1", "Hembra"),
        ("2", "Hembra Castrada"),
        ("3", "Macho"),
        ("4", "Macho Castrado"),
    )

    sexo = models.CharField(max_length=50, choices=sexo_choices)
    fech_naci = models.DateField(auto_now=False, auto_now_add=False)
    microchip = models.IntegerField()

    def __str__(self):
        return f'Nombre:  {self.nombre} - Dueño : {self.dueno.user.first_name.title()} {self.dueno.user.last_name.title()}'

# Funcion para validar dia 
def validar_dia(value):
    today = date.today()
    weekday = date.fromisoformat(f'{value}').weekday()

    if value < today:
        raise ValidationError('No se puede elegir una fecha tarde')
    if (weekday == 5) or (weekday == 6):
        raise ValidationError('Eliga un dia habil de la semana.')

# Tabla agenda disponibilidad atencion
class Agenda(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,default=1)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE, related_name='agenda', blank=True, null=True)
    peluquera = models.ForeignKey(Peluquera, on_delete=models.CASCADE, related_name='agenda', blank=True, null=True)
    dia = models.DateField(help_text="Ingrese una fecha para agendar")

    HORARIOS = (
        ("1", "09:00 a 10:00"),
        ("2", "10:00 a 11:00"),
        ("3", "11:00 a 12:00"),
        ("4", "12:00 a 13:00"),
        ("5", "13:00 a 14:00"),
    )
    horario = models.CharField(max_length=10, choices=HORARIOS)

    class Meta:
        unique_together = ('horario', 'dia')

    def __str__(self):
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        mes = self.dia.strftime("%B").capitalize()
        locale.setlocale(locale.LC_TIME, '')
        return f'{mes} {self.dia.day} {self.dia.year} - {self.get_horario_display()} - Categoria: {self.categoria.nombre}'

# Tabla de agendamiento
class Agendamiento(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=12)
    correo = models.EmailField()
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
    