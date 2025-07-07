from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware
import mysql.connector
from mysql.connector import Error
import schemas

app = FastAPI(
    title="ms-gestion-gestor",
    description="Microservicio para la gestión de gestores",
    version="1.0.0"
)

origins = ['*'] # Permite que el Api Rest se consuma desde cualquier origen

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

host_name = os.getenv("MYSQL_HOST", "localhost")  # Use mysql container in Docker
port_number = os.getenv("MYSQL_PORT", "3306")
user_name = os.getenv("MYSQL_USER", "root")
password_db = os.getenv("MYSQL_PASSWORD", "root")
database_name = os.getenv("MYSQL_DATABASE", "db_poliza")

# Get echo test for load balancer's health check
@app.get("/health", tags=["Health Check"])
def get_echo_test():
    return {"data": None, "success": True, "errorMessage": None }

# Get all polizas
@app.get("/gestores", tags=["Gestores"])
def get_gestores():
    try:
        # Connect to the database
        mydb = mysql.connector.connect(
            host=host_name,
            port=port_number,
            user=user_name,
            password=password_db,
            database=database_name
        )

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM gestor")
        result = cursor.fetchall()
        cursor.close()
        mydb.close()

        print(f"Result from database: {result}")  # Debug print

        gestores = []
        if result:
            for row in result:
                print(f"Processing row: {row}")  # Debug print
                gestor_dict = {
                    "id": row[0],
                    "codigo_gestor": row[1],
                    "nombre": row[2],
                    "documento": row[3],
                    "tipo_documento": row[4],
                    "peso": row[5]
                }
                gestor_out = schemas.gestor(**gestor_dict)
                gestores.append(gestor_out.dict())

        return {"data": gestores, "success": True, "errorMessage": None }

    except Error as e:
        # Catch database-related errors
        return {"data": None, "success": False, "errorMessage": f"MySQL Error: {e}"}

    except Exception as e:
        # Catch any other errors
        return {"data": None, "success": False, "errorMessage": f"Unexpected error: {str(e)}"}

# Get an poliza by persona ID
@app.get("/gestor/{codigo_gestor}", tags=["Gestores"])
def get_gestor(codigo_gestor: str):
    try:
        mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)  
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM gestor WHERE codigo_gestor = %s", (codigo_gestor,))
        result = cursor.fetchall()
        cursor.close()
        mydb.close()
        
        gestor = []
        if result:
            for row in result:
                gestor_dict = {
                    "id": row[0],
                    "codigo_gestor": row[1],
                    "nombre": row[2],
                    "documento": row[3],
                    "tipo_documento": row[4],
                    "peso": row[5]
                }
                gestor_out = schemas.gestor(**gestor_dict)
                gestor.append(gestor_out.dict())
            
            return {"data": gestor, "success": True, "errorMessage": None }
        else:
            return {"data": None, "success": False, "errorMessage": "Producto no encontrado"}
    except Error as e:
        return {"data": None, "success": False, "errorMessage": f"MySQL Error: {e}"}
    except Exception as e:
        return {"data": None, "success": False, "errorMessage": f"Unexpected error: {str(e)}"}

# Configuración para fastapi dev
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6005, reload=True)
