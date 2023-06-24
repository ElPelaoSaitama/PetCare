from django.contrib import admin
from .models import *

# Register your models here.

class EspecieAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  # Campos a mostrar en la lista de registros
    list_filter = ('nombre',)  # Campos por los que se puede filtrar
    search_fields = ('nombre',)  # Campos por los que se puede buscar

class RazaAdmin(admin.ModelAdmin):
    list_display = ('especie', 'nombre')  # Campos a mostrar en la lista de registros
    list_filter = ('especie',)  # Campos por los que se puede filtrar
    search_fields = ('nombre', 'especie__nombre')  # Campos por los que se puede buscar
    list_per_page = 15  # Número de registros a mostrar por página
    ordering = ('especie', 'nombre')  # Orden de los registros en la lista
    autocomplete_fields = ['especie']  # Campos con autocompletado
    readonly_fields = ('id',)  # Campos solo de lectura



admin.site.register(Raza, RazaAdmin)
admin.site.register(Especie, EspecieAdmin)
admin.site.register(Categoria)
admin.site.register(Veterinario)
admin.site.register(Peluquera)
admin.site.register(Agendamiento)
admin.site.register(Contacto)
admin.site.register(Cliente)
admin.site.register(Mascota)
admin.site.register(Agenda)
admin.site.register(Genero)
admin.site.register(Diagnostico)