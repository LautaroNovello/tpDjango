## 1. Creación del Dockerfile
Lo primero que hacemos es definir el docker-compose.yaml, donde levantamos 4 contenedor:
- 🗄️ **Base de datos:** PostgreSQL
- 🖥️ **Backend:** Django
- 🛠️ **Generate:** crea el proyecto Django automáticamente
- ⚙️ **Manage:** utilidad para ejecutar comandos de Django
```dockerfile
services:
  db:
    image: postgres:alpine
    env_file:
      - .env.db
    environment:
      - POSTGRES_INITDB_ARGS=--auth-host=md5 --auth-local=trust
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready" ]
      interval: 10s
      timeout: 2s
      retries: 5
    volumes:
      - postgres-db:/var/lib/postgresql/data
    networks:
      - net

  backend:
    build: .
    command: runserver 0.0.0.0:8000
    entrypoint: python3 manage.py
    env_file:
      - .env.db
    expose:
      - "8000"
    ports:
      - "8000:8000"
    volumes:
      - ./src:/code
    depends_on:
      db:
        condition: service_healthy
    networks:
      - net

  generate:
    build: .
    user: root
    command: /bin/sh -c 'mkdir src && django-admin startproject app src'
    env_file:
      - .env.db
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/code
    networks:
      - net

  manage:
    build: .
    entrypoint: python3 manage.py
    env_file:
      - .env.db
    volumes:
      - ./src:/code
    depends_on:
      db:
        condition: service_healthy
    networks:
      - net


networks:
  net:

volumes:
  postgres-db:
```
## 2. Definimos el archivos .init
Este archivo nos sirve para automatizar comandos, evitando ejecutarlos uno por uno manualmente.
- En Windows, usar extensión `.ps1`
- En Linux, usar extensión `.sh`

```
docker compose down -v --remove-orphans --rmi all
docker compose run --rm manage makemigrations
docker compose run --rm manage migrate
docker compose up backend -d
docker compose run --rm manage createsuperuser --noinput --username admin --email admin@example.com
docker compose run --rm manage shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u=User.objects.get(username='admin'); u.set_password('admin'); u.save()"
docker compose run --rm manage loaddata cantina/initial_data.json
```
## 3. Definimos el archivos models.py
En este archivo definimos los modelos de nuestra base de datos para luego migrarlos con Django.- Clase Categoria
```
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre
    
```
✅ El método __str__ permite que en la vista gráfica de Django se vea el nombre en lugar de "Categoria Object".
- Clase Producto
```
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
```
- Clase Venta 
```
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
    
```
✅ El método `total` se llama sin paréntesis en plantillas porque está diseñado como propiedad calculada.
- Clase DetalleVenta
```
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
```
✅ `precioHistorico` se define como no editable y se guarda automáticamente con el precio del producto en el momento de la venta para evitar inconsistencias si el precio cambia.

✅ `__str__`muestra de forma clara el producto y cantidad.

✅ El método `total` devuelve el subtotal de cada detalle de venta.

✅ El decorador `@property ` en `total`:
- Permite acceder a `detalle.total` sin paréntesis, como un atributo calculado.
- Es útil en plantillas Django y en vistas para mayor legibilidad.
- Calcula en tiempo real `cantidad * precioHistorico` sin ocupar espacio en la base de datos.

✅ El método `save`:
- Se ejecuta cada vez que guardamos una instancia (`detalle.save()`).
- Si es un nuevo detalle, guarda automáticamente el precio actual del producto como `precioHistorico`.
- Clase Empleado
```
class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    dni = models.IntegerField()
    fecha_nacimiento = models.DateField()
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
```
## 4. Definos el archivo admin.py
El archivo `admin.py` en cada aplicación de Django se utiliza para configurar qué modelos serán visibles y administrables desde el panel de administración de Django `(/admin)`.
✅ Clase `DetalleVentaInline`
```
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    readonly_fields = ('precioHistorico','total',)
    fields = ('producto', 'cantidad', 'precioHistorico', 'total')
    extra = 0

```
- Hereda de `admin.TabularInline`, que permite editar `DetalleVenta` dentro del admin de `Venta` en formato tabla.
- `readonly_fields`: los campos `precioHistorico` y `total` son de solo lectura en el admin.
- `fields`: indica qué campos mostrar en el inline, ya que si no se colocan explícitamente no aparecen.0
- `extra = 0`: no muestra formularios vacíos adicionales por defecto.

✅ Registro del modelo `Categoria`
```
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'nombre')
    search_fields = ('nombre',)
```
- `list_display`: muestra el `id` y `nombre` en la lista de categorías.
- `search_fields`: permite buscar categorías por nombre.

✅ Registro del modelo `Producto`
```
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'precio', 'stock', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

```
- `list_filter`: permite filtrar productos por categoría.

✅ Registro del modelo `Venta`
```
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id_venta', 'fecha_hora_venta', 'empleado', 'total_venta')
    list_filter = ('fecha_hora_venta', 'empleado')
    search_fields = ('empleado__nombre', 'empleado__apellido')
    inlines = [DetalleVentaInline]

    def total_venta(self, obj):
        return obj.total()
    total_venta.short_description = 'Total Venta'

```
- `inlines`: incluye `DetalleVentaInline` para poder agregar o editar detalles de venta directamente dentro de cada venta.
- `total_venta`: método para mostrar el total de la venta en la lista de ventas, calculado usando `obj.total()` del modelo.
✅ Registro del modelo `DetalleVenta`
```
@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('id_detalleVenta', 'producto', 'venta', 'cantidad', 'precioHistorico', 'total')
    list_filter = ('producto',)
    search_fields = ('producto__nombre',)

    def total(self, obj):
        return obj.total
    total.short_description = 'Total Detalle'

```
- Método `total`: retorna el subtotal del detalle (`cantidad * precioHistorico`), usando la propiedad `total` del modelo, para mostrarlo en la lista del admin.
✅ Registro del modelo `Empleado`
```
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id_empleado', 'nombre', 'apellido', 'dni', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido', 'dni')
```
## 5. Para ejecutar el proyecto
1. Bajamos el repositorio
2. En la terminal ejecutamos `docker compose up -d`
3. Luego, ejecutamos `.\init.ps1` en caso de estar en Windows y `.\init.sh` en Linux
4. Abrimos `http://localhost:8000/admin/`


