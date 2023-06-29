from django.contrib import admin
from .models import Articulo, Taller

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'costo', 'cantidad_producida_en_el_mes', 'taller', 'mes_proceso', 'cantidad_rechazada']

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ['codigo',]

