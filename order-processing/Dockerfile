# Usa una imagen de Node.js
FROM node:14

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar archivos de proyecto
COPY package*.json ./
COPY . .

# Instalar dependencias
RUN npm install

# Ejecutar el microservicio
CMD ["node", "index.js"]
