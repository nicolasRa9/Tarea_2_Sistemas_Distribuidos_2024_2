# Proyecto de Microservicios con Docker

Este proyecto implementa una arquitectura de microservicios para un sistema de gestión de pedidos, donde cada microservicio realiza una tarea específica (como gestionar pedidos, procesar pagos, enviar notificaciones y monitorear el rendimiento del sistema). La infraestructura se ejecuta en contenedores Docker, administrados mediante Docker Compose.

## Estructura del Proyecto

### Servicios Principales

- **Zookeeper** y **Kafka**: Gestionan la comunicación basada en eventos entre microservicios.
- **Elasticsearch** y **Kibana**: Almacenan y visualizan métricas de rendimiento y logs del sistema.
- **gRPC Server**: Recibe solicitudes de pedidos y las publica en Kafka.
- **Order Processing**: Escucha y procesa pedidos de Kafka, actualizando su estado.
- **Notification Service**: Envía notificaciones a los clientes cuando se actualiza el estado de sus pedidos.
- **Prometheus** y **Grafana**: Monitorean y visualizan el rendimiento del sistema.

## Pre-requisitos

- **Docker**: [Instalar Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Instalar Docker Compose](https://docs.docker.com/compose/install/)

## Configuración de Variables de Entorno

Asegúrate de configurar las variables de entorno necesarias para conectarte a servicios externos, como servidores SMTP para el envío de correos en el **Notification Service**. Crea un archivo `.env` en el directorio raíz con los siguientes datos:

```env
GRPC_SERVER_ADDRESS=grpc-server:50051
KAFKA_BROKER_1=kafka-broker-1:9092
KAFKA_BROKER_2=kafka-broker-2:9093
ELASTICSEARCH_HOST=elasticsearch
SMTP_HOST=smtp.example.com
SMTP_USER=your_email@example.com
SMTP_PASS=your_password
****
```
##Instrucciones de Ejecución

Clonar el Repositorio:
```env
bash
Copiar código
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>
```
Configuración de Elasticsearch y Prometheus:

Crea un archivo prometheus.yml en el directorio raíz para que Prometheus pueda recolectar métricas desde cAdvisor.

```env
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```
##Levantar los Contenedores
Ejecuta el siguiente comando para construir y levantar todos los servicios definidos en docker-compose.yml:

```env
docker-compose up --build
```
Este comando construirá las imágenes de Docker y levantará todos los contenedores. Los servicios estarán configurados para iniciar en el orden correcto, con Zookeeper y Kafka como primeras dependencias.

##Acceder a las Interfaces de Usuario:
-**Kibana** (para ver las métricas en Elasticsearch): http://localhost:5601


-**Prometheus** (para ver las métricas de cAdvisor): http://localhost:9090

-**Grafana** (para visualizar dashboards de rendimiento): http://localhost:3001

-**Usuario y contraseña predeterminados**: admin / admin

-**cAdvisor** (para monitorear los recursos de cada contenedor): http://localhost:8080

Detener los Contenedores
##Para detener todos los contenedores, usa:
```env
docker-compose down
Estructura de Directorios
/grpc-server: Contiene el código y configuración del servidor gRPC.
/order-processing: Código y configuración del microservicio de procesamiento de pedidos.
/notification-service: Código y configuración para el servicio de notificaciones.
/prometheus.yml: Configuración para Prometheus.
```

Notas Adicionales
Asegúrate de configurar correctamente el archivo .env con las credenciales de tu servicio SMTP si deseas que el Notification Service funcione.
El índice de Elasticsearch (performance_metrics) almacenará métricas del sistema, como tiempos de respuesta y throughput, para visualización en Kibana.
##Visualización de Métricas
-**Throughput del Sistema**: Observa el número de pedidos procesados en intervalos específicos en Grafana.
-**Latencia y Tiempo de Procesamiento**: Usa Kibana para monitorear la latencia entre eventos y el tiempo de procesamiento total en Elasticsearch.
-**Concurrencia y Cuellos de Botella**: Identifica microservicios con tiempos elevados o cuellos de botella en el procesamiento en los dashboards de Grafana.
##Solución de Problemas
Errores en los Servicios: Si algún servicio no se levanta correctamente, verifica los logs del contenedor usando:

```env
docker-compose logs <nombre_del_servicio>
```
Problemas de Conexión con Elasticsearch y Kibana: Asegúrate de que Elasticsearch esté completamente iniciado antes de iniciar Kibana. Puedes observar los logs de Elasticsearch y esperar a que indique started.

Correo Electrónico en Notification Service: Si el Notification Service no envía correos, verifica la configuración del servidor SMTP en el archivo .env y asegúrate de que la autenticación sea correcta.

Error de Red o Conexión: Asegúrate de que todos los servicios están en la misma red Docker (my-network). Puedes verificar la red ejecutando:

```env
Copiar código
docker network ls
```
Tiempo de Ejecución de gRPC Server: Si el servidor gRPC no responde, asegúrate de que el cliente tenga la dirección correcta (GRPC_SERVER_ADDRESS) y que el puerto esté mapeado en docker-compose.yml.

