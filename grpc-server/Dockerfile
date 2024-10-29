# Usar una imagen ligera de Python 3.11
FROM python:3.9

# Instalar las dependencias del sistema necesarias para compilar grpcio
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    protobuf-compiler \
    libz-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar pip, setuptools y wheel actualizado
RUN pip install --upgrade pip setuptools wheel

# Instalar las dependencias de Python desde el archivo requirements.txt
RUN pip install -r requirements.txt

# Generar los archivos gRPC a partir del archivo .proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. order_management.proto

# Exponer el puerto del servidor gRPC
EXPOSE 50051

# Comando para iniciar el servidor gRPC
CMD ["python", "order_management_server.py"]
