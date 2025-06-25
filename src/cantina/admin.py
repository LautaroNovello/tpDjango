from django.contrib import admin
from .models import Categoria, Producto, Venta, DetalleVenta, Empleado

# Register your models here.
from django.contrib import admin
from .models import Categoria, Producto, Venta, DetalleVenta, Empleado

#definimos esta clase que hereda la clase TabularInline
#que permite mostrar un formulario en linea en el admin, en formato tabla para editar los detalles de venta)
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    readonly_fields = ('precioHistorico','total',)  # campo solo lectura
    fields = ('producto', 'cantidad', 'precioHistorico', 'total')  # Hay que incluirlo explicitamente sino, no se muestra
    extra = 0

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
    list_display = ('id_venta', 'fecha_hora_venta', 'empleado', 'total_venta')
    list_filter = ('fecha_hora_venta', 'empleado')
    search_fields = ('empleado__nombre', 'empleado__apellido')
    inlines = [DetalleVentaInline]
    def total_venta(self, obj):
        return obj.total()
    total_venta.short_description = 'Total Venta'

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('id_detalleVenta', 'producto', 'venta', 'cantidad', 'precioHistorico', 'total')
    list_filter = ('producto',)
    search_fields = ('producto__nombre',)
    def total(self, obj):
        return obj.total
    total.short_description = 'Total Detalle'

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id_empleado', 'nombre', 'apellido', 'dni', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'dni')

