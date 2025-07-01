import os
import django
import sys

sys.path.append("/code")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

django.setup()
# IMPORTS DE DJANGO (MODELOS RELACIONALES)
from cantina.models import (Venta)


# IMPORTS DE MONGOENGINE (DOCUMENTOS EMBEBIDOS)
from modelos_mongo import Venta as VentaMongo
from modelos_mongo import (DetalleVentaEmb,ProductoEmb,CategoriaEmb,EmpleadoEmb)

# MIGRAR VENTAS UNA POR UNA
for venta_sql in Venta.objects.all():
    print(venta_sql)
    # === MIGRAR EMPLEADO ===
    empleado_sql = venta_sql.empleado
    empleado_emb = None
    if empleado_sql:
        empleado_emb = EmpleadoEmb(
            id_empleado=empleado_sql.id_empleado,
            nombre=empleado_sql.nombre,
            apellido=empleado_sql.apellido,
            dni=empleado_sql.dni,
            fecha_nacimiento=empleado_sql.fecha_nacimiento
        )

    # === MIGRAR DETALLES ===
    detalles_emb = []
    for detalle_sql in venta_sql.detalles.all():
        producto_sql = detalle_sql.producto
        categoria_sql = producto_sql.categoria

        # CATEGORIA embebida

        categoria_emb = CategoriaEmb(
            id_categoria=categoria_sql.id_categoria,
            nombre=categoria_sql.nombre
        )

        # PRODUCTO embebido
        producto_emb = ProductoEmb(
            id_producto=producto_sql.id_producto,
            nombre=producto_sql.nombre,
            precio=producto_sql.precio,
            stock=producto_sql.stock,
            categoria=categoria_emb
        )
        print(producto_emb)

        # DETALLE embebido
        detalle_emb = DetalleVentaEmb(
            id_detalleVenta=detalle_sql.id_detalleVenta,
            cantidad=detalle_sql.cantidad,
            precioHistorico=detalle_sql.precioHistorico,
            producto=producto_emb
        )

        detalles_emb.append(detalle_emb)

    # === CREAR DOCUMENTO DE VENTA ===
    venta_mongo = VentaMongo(
        id_venta=venta_sql.id_venta,
        fecha_hora_venta=venta_sql.fecha_hora_venta,
        empleado=empleado_emb,
        detalles=detalles_emb
    )

    venta_mongo.save()
    print(f"Venta {venta_sql.id_venta} migrada a MongoDB")
