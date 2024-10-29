# Usa una imagen de Node.js
FROM node:14

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de proyecto
COPY package*.json ./
RUN npm install
COPY . .

# Expone el puerto 3000 para el servicio HTTP
EXPOSE 3000

# Comando para ejecutar el microservicio
CMD ["node", "index.js"]
