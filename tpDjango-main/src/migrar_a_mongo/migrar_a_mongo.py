import os
import django
import sys

sys.path.append("/code")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

django.setup()
# Estos imports deben hacerse despues de django.setup()
from cantina.models import (Venta,DetalleVenta,Producto,Categoria,Empleado)
from modelos_mongo import Venta as VentaMongo #importamos asi no tenemos probleam con venta del modelo psql
from modelos_mongo import (DetalleVentaEmb,ProductoDoc,CategoriaDoc,EmpleadoDoc)

# migrar ventas una por una
for venta_sql in Venta.objects.all():

    # aniadir empleado
    empleado_sql = venta_sql.empleado
    empleado_id = None #declaro el empleado antes de asignarlo a al documento de empleado,por si no lo encuentra
    if empleado_sql:
        empleado_id = empleado_sql.id_empleado

    # migracion de detalles
    detalles_emb = []
    for detalle_sql in venta_sql.detalles.all():
        producto_sql = detalle_sql.producto
        categoria_sql = producto_sql.categoria

        # creacion del documento embedded de detalle venta
        detalle_emb = DetalleVentaEmb(
            id_detalleVenta=detalle_sql.id_detalleVenta,
            cantidad=detalle_sql.cantidad,
            subtotal=detalle_sql.precioHistorico * detalle_sql.cantidad,  # Guardamos el subtotal
            producto= producto_sql.id_producto 
        )

        detalles_emb.append(detalle_emb)

    # creacion del documento de venta 
    ventas = VentaMongo(
        id_venta=venta_sql.id_venta,
        fecha_hora_venta=venta_sql.fecha_hora_venta,
        empleado=empleado_id,
        detalles=detalles_emb
    )

    ventas.save()



#Migracion de productos
productos_emb = Producto.objects.all()
#Migramos solo los productos que no existen(migracion incremental)
for producto in productos_emb:
    if not ProductoDoc.objects.filter(id_producto=producto.id_producto).first():
        productos = ProductoDoc(
            id_producto=producto.id_producto,
            nombre=producto.nombre,
            precio=producto.precio,
            stock=producto.stock,
            categoria = producto.categoria.id_categoria  # Asignamos la referencia a la categoria
        )
        productos.save()
        print("Producto migrado")

#Migracion de categorias
categorias_emb = Categoria.objects.all()
for categoria in categorias_emb:
    if not CategoriaDoc.objects.filter(id_categoria=categoria.id_categoria).first():
        categorias = CategoriaDoc(
            id_categoria=categoria.id_categoria, 
            nombre=categoria.nombre)
        categorias.save()
        print("Categoria migrada")

#Migracion de empleados
empleados_emb = Empleado.objects.all()
for empleado in empleados_emb:
    if not EmpleadoDoc.objects.filter(id_empleado=empleado.id_empleado).first():
        empleados = EmpleadoDoc(
            id_empleado=empleado.id_empleado,
            nombre=empleado.nombre,
            apellido=empleado.apellido,
            dni=empleado.dni,
            fecha_nacimiento=empleado.fecha_nacimiento
        )
        empleados.save()
        print("Empleado migrado")



