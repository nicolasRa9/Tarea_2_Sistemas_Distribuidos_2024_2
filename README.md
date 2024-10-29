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
