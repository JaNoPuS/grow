"""
    INVENTARIO VIEWS
"""

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductoForm, CategoriaForm
from .models import Producto, Categoria, MovimientosInventario

def inventario_index(request):
    return render(request, 'inventarioApp/inventario_index.html')

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventarioApp:lista_categorias')
    else:
            form = CategoriaForm()
    return render(request, 'inventarioApp/crear_categoria.html', {'form': form})

def lista_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'inventarioApp/lista_categorias.html', {'categorias': categorias})

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventarioApp/lista_productos.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventarioApp:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventarioApp/crear_producto.html', {'form': form})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('inventarioApp:lista_productos')
    
    return render(request, 'inventarioApp/eliminar_producto.html', {'producto': producto})

def actualizar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    cantidad_anterior = producto.cantidad_disponible

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            nueva_cantidad = producto.cantidad_disponible
            if nueva_cantidad != cantidad_anterior:
                if nueva_cantidad > cantidad_anterior:
                    tipo_movimiento = 'entrada'
                else:
                    tipo_movimiento = 'salida'
                cantidad_movimiento = abs(nueva_cantidad - cantidad_anterior)
                MovimientosInventario.registrar_movimiento(producto, tipo_movimiento, cantidad_movimiento)
            form.save()
            return redirect('inventarioApp:lista_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'inventarioApp/actualizar_producto.html', {'form': form, 'producto': producto})

