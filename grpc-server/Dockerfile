# Dockerfile para el microservicio gRPC
FROM python:3.9-slim

# Instalar las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del servidor gRPC
COPY . /app

# Instalar las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto para el servidor gRPC
EXPOSE 50051

# Comando para iniciar el servidor gRPC
CMD ["python", "order_management_server.py"]
