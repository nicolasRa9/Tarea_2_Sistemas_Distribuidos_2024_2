# Dockerfile para el microservicio de pagos
FROM node:16

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos package.json y package-lock.json
COPY package*.json ./

# Instalar las dependencias
RUN npm install

# Copiar el resto de los archivos de la aplicación
COPY . .

# Exponer el puerto (opcional si es necesario)
EXPOSE 3000

# Comando para iniciar el microservicio
CMD ["node", "paymentService.js"]

