from mongoengine import (Document, EmbeddedDocument, EmbeddedDocumentField,StringField, IntField, DecimalField, DateTimeField,
DateField, ListField)

from decimal import Decimal
from mongoengine import connect

connect('ventas', host='mongo', port=27017)

# === EmbeddedDocument: Categoria ===
class CategoriaEmb(EmbeddedDocument):
    id_categoria = IntField(required=True)
    nombre = StringField(required=True)

    def __str__(self):
        return self.nombre

# === EmbeddedDocument: Producto ===
class ProductoEmb(EmbeddedDocument):
    id_producto = IntField(required=True)
    nombre = StringField(required=True)
    precio = DecimalField(precision=2, force_string=True, required=True)
    stock = IntField(required=True)
    categoria = EmbeddedDocumentField(CategoriaEmb, required=True)

    def __str__(self):
        return self.nombre

# === EmbeddedDocument: Empleado ===
class EmpleadoEmb(EmbeddedDocument):
    id_empleado = IntField(required=True)
    nombre = StringField(required=True)
    apellido = StringField(required=True)
    dni = IntField(required=True)
    fecha_nacimiento = DateField(required=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# === EmbeddedDocument: DetalleVenta ===
class DetalleVentaEmb(EmbeddedDocument):
    id_detalleVenta = IntField(required=True)
    cantidad = IntField(required=True)
    precioHistorico = DecimalField(precision=2, force_string=True, required=True)
    producto = EmbeddedDocumentField(ProductoEmb, required=True)

    def __str__(self):
        return f"{self.producto} - Cantidad: {self.cantidad}"

    @property
    def total(self):
        return self.cantidad * self.precioHistorico

# === Documento principal: Venta ===
class Venta(Document):
    id_venta = IntField(required=True, primary_key=True)
    fecha_hora_venta = DateTimeField(required=True)
    empleado = EmbeddedDocumentField(EmpleadoEmb, null=True)
    detalles = ListField(EmbeddedDocumentField(DetalleVentaEmb))

    def __str__(self):
        return str(self.id_venta)

    @property
    def total(self):
        return sum(detalle.total for detalle in self.detalles)
