===================================================
 MIGRACIÓN DE DATOS DE POSTGRESQL A MONGODB
===================================================
Este módulo permite migrar los datos generados en una base de datos relacional (PostgreSQL) hacia una base 
de datos documental (MongoDB), utilizando Python, Docker y el ODM MongoEngine. Es ideal para mantener 
actualizada una réplica en Mongo de los datos gestionados originalmente por Django y PostgreSQL.

===================================================
¿QUÉ ES MONGO ENGINE?
===================================================
MongoEngine es un Object-Document Mapper (ODM), que funciona como un "ORM para MongoDB". Mientras que un ORM 
(Object-Relational Mapper) como el de Django permite interactuar con bases de datos relacionales (como PostgreSQL)
usando objetos Python, MongoEngine cumple la misma función pero para bases de datos documentales como MongoDB. En otras 
palabras, MongoEngine nos ayuda a traducir los modelos relacionales de Django a documentos Mongo.

MongoDB no utiliza tablas ni relaciones como una base SQL; en su lugar, guarda información en documentos con estructura 
JSON agrupados en colecciones. MongoEngine nos permite:

**Definir documentos MongoDB como clases en Python.

**Validar automáticamente los tipos de datos.

**Consultar, insertar, actualizar y eliminar datos con una sintaxis clara y orientada a objetos.

**Mantener la lógica de negocio en Python sin tener que escribir comandos nativos de MongoDB.

===================================================
🔧 REQUISITOS PREVIOS
===================================================

Antes de realizar la migración, debemos asegurarnos de contar con lo siguiente:

✔ Proyecto funcionando correctamente con Docker.
✔ Los siguientes servicios deben estar levantados:
    - manage (Django)
    - db (PostgreSQL)
    - mongo (MongoDB)

✔ MongoEngine incluido en requirements.txt:
    mongoengine>=0.27.0

✔ El servicio de Mongo declarado en docker-compose.yml:
    mongo:
      image: mongo
      ports:
        - "27017:27017"


===================================================
 🗂️ ESTRUCTURA DE ARCHIVOS UTILIZADOS
===================================================

    migrar_a_mongo/
├── __init__.py
    Archivo que convierte la carpeta en módulo de Python.

├── modelos_mongo.py
    Contiene las definiciones de documentos Mongo usando MongoEngine.
    Ejemplo:
        class VentaMongo(Document):
            id_venta = StringField(required=True)
            fecha = DateTimeField()
            total = FloatField()
            cliente = StringField()
            meta = {'collection': 'venta'}

├── utils.py
    Funciones auxiliares para transformar los modelos de Django en objetos compatibles con Mongo.
    Ejemplo: formatear fechas, calcular campos derivados.

├── migrar_a_mongo.py
    Script principal de migración.
    - Conecta a Mongo.
    - Consulta los modelos de Django (PostgreSQL).
    - Verifica si los datos ya existen en Mongo.
    - Si no existen, los inserta.

===================================================
 DESCRIPCIÓN DEL PROCESO
===================================================
Al levantar el entorno, se precargan varias entidades en la base de datos PostgreSQL mediante fixtures o datos insertados por Django.
1. El entorno se levanta con:
   ```bash
    docker compose up -d
    ```

Podés agregar más datos desde:

**El panel de administrador de Django.

**La consola SQL de PostgreSQL.

Cuando los datos estén listos para ser migrados, simplemente ejecutás un script Python que se encarga de transferirlos a MongoDB.
Este script realiza una migración incremental: solo incluye los datos nuevos o modificados.

===================================================
 COMANDO PARA EJECUTAR LA MIGRACIÓN
===================================================

Desde la raíz del proyecto, ejecutar:
```bash
docker compose run --rm --entrypoint python3 manage /code/migrar_a_mongo/migrar_a_mongo.py
```
Este comando corre el script Python dentro del contenedor manage (Django).

===================================================
 VISUALIZAR LOS DATOS EN MONGODB
===================================================

Ingresar al shell de MongoDB con:
```bash
docker compose exec mongo mongosh
```
Luego, ejecutar:
``` bash
> show dbs
```
```bash
> use cantina
```
``` bash
> show collections
```
``` bash
> db.venta.find()
```
===================================================
✅ VENTAJAS DE MongoDB CON MONGOENGINE
===================================================
**Modelo flexible: No requiere esquemas estrictos; los documentos pueden tener estructuras distintas entre sí.

**Ideal para datos no estructurados: Perfecto para almacenar JSONs anidados, arrays, o estructuras complejas.

**Alta escalabilidad horizontal: Diseñado para crecer fácilmente con grandes volúmenes de datos y múltiples servidores.

**Velocidad en lectura y escritura: Muy eficiente cuando no se requiere consistencia transaccional fuerte.

**Desacoplamiento: Permite separar la lógica relacional (Django + PostgreSQL) del análisis o visualización documental.

===================================================
❌ DESVENTAJAS DE MongoDB CON MONGOENGINE
===================================================
**Sin integridad referencial: No hay claves foráneas ni restricciones entre documentos. La consistencia depende del código.

**Menor robustez transaccional: No es lo ideal si necesitás múltiples operaciones atómicas entre documentos.

**Más trabajo manual para relaciones: Si querés simular relaciones entre documentos, tenés que hacerlo desde el código.

**Menor integración con Django nativo: No reemplaza el ORM de Django, sino que se usa por fuera para otras tareas.
===================================================
 CONCLUSIÓN
===================================================

- El script puede ejecutarse múltiples veces sin duplicar datos.
- Si se agregan modelos nuevos, deben reflejarse en modelos_mongo.py.
- Usamos MongoEngine para tener validación de campos y consultas limpias.
- Este enfoque permite mantener Mongo actualizado con PostgreSQL de manera controlada.

