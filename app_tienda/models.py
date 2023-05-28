from django.db import models

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
    