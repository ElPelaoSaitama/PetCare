from django.contrib import admin
from .models import *
from .forms import ProductoForm


class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "precio", "categoria", "subCategoria"]
    list_editable = ["precio", "categoria", "subCategoria"]
    #form = ProductoForm



admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)
