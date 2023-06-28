from django.urls import path
from . import views  

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar_articulo/', views.agregar_articulo, name='agregar_articulo'),
    path('actualizar_articulo/<pk>', views.actualizar_articulo, name='actualizar_articulo'),
    path('eliminar_articulo/<pk>', views.eliminar_articulo, name='eliminar_articulo'),
    path('taller/<pk>', views.taller, name='taller'),
    path('acerca_de/', views.acerca_de, name='acerca_de'),
    path('buscar_rango_fecha/', views.buscar_rango_fecha, name='buscar_rango_fecha'),
]
