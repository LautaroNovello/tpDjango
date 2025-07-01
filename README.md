# Migración de Datos de PostgreSQL a MongoDB

Este proyecto permite migrar datos desde una base de datos relacional en PostgreSQL a una base de datos documental en MongoDB, utilizando un script de python.

---

## 🔧 Requisitos previos

Antes de realizar la migración, es necesario asegurarse de lo siguiente:

1. Haber seguido correctamente las instrucciones del `README` del proyecto principal (`main`), lo cual incluye levantar el entorno completo.
2. Que el contenedor de MongoDB esté funcionando correctamente.
3. Tener en ejecución los **3 contenedores necesarios** del proyecto mediante Docker Compose.
4. Tener añadido MongoEngine en requirements.txt

---

## 🗃️ Descripción del Proceso

Al levantar el entorno por primera vez, el sistema precarga varias entidades en la base de datos PostgreSQL.  
El siguiente paso será migrar dichos datos a MongoDB.

---

## 🚀 Comando para ejecutar la migración

Para ejecutar el proceso de migración, utilizar el siguiente comando en la raíz del proyecto:

```bash
docker compose run --rm --entrypoint python3 manage /code/migrar_a_mongo/migrar_a_mongo.py
