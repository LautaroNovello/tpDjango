from django.db import models

# | Campo                                           | Lo que crea                   |
# | ----------------------------------------------- | ----------------------------- |
# | `CharField(max_length=200)`                     | VARCHAR                       |
# | `TextField()`                                   | TEXT                          |
# | `IntegerField()`                                | INTEGER                       |
# | `DecimalField(max_digits=10, decimal_places=2)` | DECIMAL                       |
# | `DateField()`                                   | DATE                          |
# | `EmailField()`                                  | VARCHAR + validación de email |
# | `BooleanField()`                                | BOOLEAN                       |
# | `ForeignKey()`                                  | Relación UNO a MUCHOS         |
# | `ManyToManyField()`                             | Relación MUCHOS a MUCHOS      |
# | `OneToOneField()`                               | Relación UNO a UNO            |

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos'
    )

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_hora_venta = models.DateTimeField()
    empleado = models.ForeignKey(
        'Empleado',
        on_delete=models.CASCADE,
        related_name='ventas',
        null=True,
        blank=True
    )

class DetalleVenta(models.Model):
    id_detalleVenta = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    precioHistorico = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='detalles_venta'
    )
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.IntegerField()
    fecha_nacimiento = models.DateField()
