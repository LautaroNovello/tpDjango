from django.contrib import admin
from .models import Categoria, Producto, Venta, DetalleVenta, Empleado

# Register your models here.
from django.contrib import admin
from .models import Categoria, Producto, Venta, DetalleVenta, Empleado

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'nombre')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'precio', 'stock', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id_venta', 'fecha_hora_venta', 'empleado')
    list_filter = ('fecha_hora_venta', 'empleado')
    search_fields = ('empleado__nombre', 'empleado__apellido')

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('id_detalleVenta', 'producto', 'venta', 'cantidad', 'precioHistorico')
    list_filter = ('producto',)
    search_fields = ('producto__nombre',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id_empleado', 'nombre', 'apellido', 'dni', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'dni')

