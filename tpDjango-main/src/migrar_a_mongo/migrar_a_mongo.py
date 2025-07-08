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
    empleado_id = None #por si no lo encuentra
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
ids_postgres = set(Venta.objects.values_list('id_venta', flat=True))
ids_mongo = set(doc.id_venta for doc in VentaMongo.objects.only('id_venta'))
ventas_a_eliminar = ids_mongo - ids_postgres
for id_venta in ventas_a_eliminar:
    VentaMongo.objects.filter(id_venta=id_venta).delete()
    print(f"Venta eliminada: {id_venta}")


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
#Buscar ids en postgre
ids_postgres = set(Producto.objects.values_list('id_producto', flat=True))
#Buscar ids en mongo
ids_mongo = set(doc.id_producto for doc in ProductoDoc.objects.only('id_producto'))
#objetos que están en mongo pero ya no en Ppostgre
productos_a_eliminar = ids_mongo - ids_postgres
for id_prod in productos_a_eliminar:
    ProductoDoc.objects.filter(id_producto=id_prod).delete()
    print(f"Producto eliminado: {id_prod}")


#Migracion de categorias
categorias_emb = Categoria.objects.all()
for categoria in categorias_emb:
    if not CategoriaDoc.objects.filter(id_categoria=categoria.id_categoria).first():
        categorias = CategoriaDoc(
            id_categoria=categoria.id_categoria, 
            nombre=categoria.nombre)
        categorias.save()
        print("Categoria migrada")

ids_postgres = set(Categoria.objects.values_list('id_categoria', flat=True))
ids_mongo = set(doc.id_categoria for doc in CategoriaDoc.objects.only('id_categoria'))
categorias_a_eliminar = ids_mongo - ids_postgres
for id_cat in categorias_a_eliminar:
    CategoriaDoc.objects.filter(id_categoria=id_cat).delete()
    print(f"Categoría eliminada: {id_cat}")


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
ids_postgres = set(Empleado.objects.values_list('id_empleado', flat=True))
ids_mongo = set(doc.id_empleado for doc in EmpleadoDoc.objects.only('id_empleado'))
empleados_a_eliminar = ids_mongo - ids_postgres
for id_emp in empleados_a_eliminar:
    EmpleadoDoc.objects.filter(id_empleado=id_emp).delete()
    print(f"Empleado eliminado: {id_emp}")


