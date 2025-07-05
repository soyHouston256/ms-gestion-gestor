# ms-gestion-gestor/Dockerfile
FROM python:3.11-slim

LABEL maintainer="Pacífico Health Insurance Team"
LABEL description="MS Gestión Gestor - Microservicio para gestión de gestores"

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de configuración de proyecto
COPY pyproject.toml* ./
COPY requirements.txt* ./

# Crear requirements.txt desde pyproject.toml o crear uno básico
RUN if [ -f pyproject.toml ]; then \
    pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir build; \
    else \
    echo "fastapi==0.104.1" > requirements.txt && \
    echo "uvicorn[standard]==0.24.0" >> requirements.txt && \
    echo "pydantic==2.5.0" >> requirements.txt; \
    fi

# Instalar dependencias básicas de FastAPI
RUN pip install --no-cache-dir fastapi uvicorn[standard] pydantic

# Copiar código fuente
COPY . .

# Instalar dependencias desde requirements.txt si existe, o usar las básicas
RUN if [ -f requirements.txt ]; then \
    pip install --no-cache-dir -r requirements.txt; \
    else \
    pip install --no-cache-dir fastapi uvicorn[standard] pydantic; \
    fi

# Crear usuario no-root
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Exponer puerto
EXPOSE 6000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:6000/ || exit 1

# Comando por defecto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6000", "--reload"]
