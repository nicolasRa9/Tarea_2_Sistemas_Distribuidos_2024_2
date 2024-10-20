# Dockerfile para el microservicio de procesamiento en Node.js
FROM node:16

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos package.json y package-lock.json antes de instalar dependencias
COPY package*.json ./

# Instalar las dependencias
RUN npm install

# Copiar el resto de los archivos de la aplicación
COPY . .

# Exponer el puerto (opcional si es necesario para debug o monitorización)
EXPOSE 3000

# Comando para iniciar el servicio
CMD ["node", "orderProcessingService.js"]
