"""
    INVENTARIO URLS
"""

from django.urls import path
from . import views

app_name = 'inventarioApp'

urlpatterns = [
    path('', views.inventario_index, name='inventario_index'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear', views.crear_producto, name='crear_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/actualizar/<int:id>/', views.actualizar_producto, name='actualizar_producto'),
    path('productos/categorias/', views.lista_categoria, name='lista_categorias'), 
    path('productos/categorias/crear', views.crear_categoria, name='crear_categoria'),
]