# api-personas

## Requisitos

- Python 3.8 o superior
- MySQL (servidor de base de datos)
- (Opcional) Docker

## Instalación y ejecución local

1. **Clona el repositorio:**
   ```bash
   git clone <URL_DEL_REPO>
   cd ms-gestion-poliza
   ```

2. **Instala las dependencias:**
   ```bash
   pip install fastapi[standard] pydantic mysql-connector-python
   ```

3. **Configura la base de datos:**
   - Asegúrate de tener un servidor MySQL corriendo.
   - Ejecuta el archivo `db.txt` en tu gestor de base de datos para crear la base y las tablas de ejemplo.

4. **Configura la conexión a la base de datos:**
   - Edita los valores de `host_name`, `port_number`, `user_name`, `password_db` y `database_name` en `main.py` según tu entorno.

5. **Ejecuta el servidor:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

6. **Accede a la API:**
   - Documentación interactiva: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Ejecución con Docker

1. **Construye la imagen:**
   ```bash
   docker build -t api-personas .
   ```

2. **Ejecuta el contenedor:**
   ```bash
   docker run -p 8000:8000 api-personas
   ```
   > Asegúrate de que la base de datos MySQL sea accesible desde el contenedor y que los parámetros de conexión estén correctamente configurados en `main.py`.

---

## Endpoints principales

- `GET /personas` — Lista todas las personas
- `GET /personas/{id}` — Obtiene una persona por ID
- `POST /personas` — Agrega una nueva persona
- `GET /polizas_persona/{id}` — Polizas por persona
- `POST /polizas` — Agrega una nueva póliza

---

## Notas

- Puedes modificar y ampliar el archivo `db.txt` para crear tus propios datos de prueba.
- Si tienes dudas sobre la estructura de la base de datos, revisa los modelos en `schemas.py`.