# Migración de Datos de PostgreSQL a MongoDB

Este proyecto permite migrar datos desde una base de datos relacional en PostgreSQL a una base de datos documental en MongoDB, utilizando un script de python.

---

## 🔧 Requisitos previos

Antes de realizar la migración, es necesario asegurarse de lo siguiente:

1. Haber seguido correctamente las instrucciones del `README` del proyecto principal (`main`), lo cual incluye levantar el entorno completo.Si nos dice que algún puerto ya está en uso,podemos ejecutar el siguiente comando para reiniciar docker:
   ```bash
   systemctl restart docker
   ```
2. Veriifcar que los **3 contenedores necesarios** esten corriendo apropiadamente.
3. Tener añadido MongoEngine en requirements.txt
4. Tener añadido el comando que ejecuta el servicio de mongo en el docker-compose.yaml
   
---

## 🗃️ Descripción del Proceso

Al levantar el entorno por primera vez, el sistema precarga varias entidades en la base de datos PostgreSQL. También podremos añadir nuevos datos desde el panel de administrador de Django, o directamente desde la consola SQL de postgres.
Una vez que los datos están listos,podremos hacer la migración a Mongo, tan solo ejecutando un script de python. Cada vez que queremos actulizar la base de datos documental,utilizaremos ese script, que hará una migración **incremental**, es decir, solo incluye los datos modificados.

---

## 🚀 Comando para ejecutar la migración

Para ejecutar el proceso de migración, utilizar el siguiente comando en la raíz del proyecto:
```bash
docker compose run --rm --entrypoint python3 manage /code/migrar_a_mongo/migrar_a_mongo.py
```

---

## **Visualizar los datos en Mongo**

Entrar en la consola de mongo:
```bash
docker compose exec mongo mongosh
```
Mostrar las bases de datos:
```bash
show dbs
```
Entrar en una base de datos:
```bash
use cantina
```
Mostrar las colecciones de esa base de datos(el símil a las tablas en relacionales):
```bash
show collections
```
Mostrar todos los datos de esa colección:
```bash
db.venta.find()
```
