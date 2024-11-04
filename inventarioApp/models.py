"""
    INVENTARIO MODELS
"""

from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos")
    cantidad_disponible = models.IntegerField()
    cantidad_minima = models.IntegerField()
    imagen = models.ImageField(upload_to='productos', blank=True, null=True)
    estado = models.CharField(max_length=20, default="nuevo", choices=[
        ('nuevo','Nuevo'),
        ('disponible','Disponible'),
        ('agotado','Agotado')
    ])

    def __str__(self):
        return self.nombre
    
    def stock_bajo(self):
        return self.cantidad_disponible <= self.cantidad_minima
    
    def mensaje_stock_bajo(self):
        if self.stock_bajo():
            return f"Advertencia: El producto '{self.nombre}' está por agotarse.\nStock actual: {self.cantidad_disponible}."

class MovimientosInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=20, choices=[
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ])
    cantidad_movimiento = models.IntegerField()
    fecha_movimiento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Movimiento: {self.tipo_movimiento} de {self.cantidad_movimiento} para {self.producto.nombre} el {self.fecha_movimiento}."
    
    @classmethod
    def registrar_movimiento(cls, producto, tipo_movimiento, cantidad_movimiento):
        if tipo_movimiento == 'salida' and cantidad_movimiento > producto.cantidad_disponible:
            raise ValueError("No hay suficiente stock disponible para este movimiento.")
        
        movimiento = cls.objects.create(
            producto=producto,
            tipo_movimiento=tipo_movimiento,
            cantidad_movimiento=cantidad_movimiento,
            fecha_movimiento=timezone.now()
        )

        if tipo_movimiento == 'entrada':
            producto.cantidad_disponible += cantidad_movimiento
        elif tipo_movimiento == 'salida':
            producto.cantidad_disponible -= cantidad_movimiento

        producto.save()
        return movimiento