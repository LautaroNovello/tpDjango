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
    def __str__(self):
        return self.nombre

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
    def __str__(self):
        return self.nombre

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
    def __str__(self):
        return str(self.id_venta)
    #como total es un atributo, no hay que llamarlo como una funcion, por eso va sin los ()
    def total(self):
        return sum(detalle.total for detalle in self.detalles.all())
    

class DetalleVenta(models.Model):
    id_detalleVenta = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    precioHistorico = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
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
    def __str__(self):
        return str(self.producto) + " - Cantidad: " + str(self.cantidad)
    #@property permite mostrar este metodo como atributo
    @property
    def total(self):
        if self.cantidad is None or self.precioHistorico is None:
            return 0  # o None, si preferís dejarlo sin valor
        return self.cantidad * self.precioHistorico
    def save(self, *args, **kwargs):
        # Solo si es un nuevo detalle (aún no guardado en la base) y no tiene precioHistorico asignado:
        if not self.pk and not self.precioHistorico:
            # Copio el precio del producto en ese momento a precioHistorico
            self.precioHistorico = self.producto.precio
        # Guardo el detalle como normalmente se hace
        super().save(*args, **kwargs)


class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.IntegerField()
    fecha_nacimiento = models.DateField()
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
