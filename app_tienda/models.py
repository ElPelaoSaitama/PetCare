from django.db import models
from django.contrib.auth.models import User

#Tabla de categorias (Perros, Gatos, Animales Exoticos, ETC)
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

#Tabla de sub categorias (Alimentos, Juguetes, Accesorios, ETC)
class SubCategoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

#Tabla de marcas
class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

#Tabla de productos
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.TextField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    subCategoria = models.ForeignKey(SubCategoria, on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to="productos", null=True)

    def __str__(self):
        return self.nombre


class Orden(models.Model):
    ordernum = models.CharField(max_length=9, null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return  f'{self.customer} - {self.ordernum}'

class Orden_detail(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cant = models.IntegerField(default=1)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)

    def __str__(self):
         return f"{self.producto.nombre} - Cantidad: {self.cant} - Orden {self.orden}"
    