from django.contrib import admin
from .models import *


class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "precio", "categoria", "subCategoria"]
    list_editable = ["precio", "categoria", "subCategoria"]



admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)
