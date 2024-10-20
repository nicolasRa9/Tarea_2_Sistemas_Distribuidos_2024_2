import grpc
from concurrent import futures
import time
import order_management_pb2_grpc as pb2_grpc
import order_management_pb2 as pb2
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import json
import uuid
import logging

# Configurar logging para mostrar mensajes en la consola
logging.basicConfig(level=logging.INFO)

# Clase que implementa el servicio gRPC
class OrderManagementService(pb2_grpc.OrderManagementServicer):
    
    def __init__(self):
        # Configura el productor de Kafka
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # Configura el cliente de Elasticsearch
        self.es = Elasticsearch(
            [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],  # Agregar esquema http
            headers={"Content-Type": "application/json"}  # Forzar uso de Content-Type compatible
        )

    def CreateOrder(self, request, context):
        # Crear un ID único para el pedido
        order_id = str(uuid.uuid4())

        # Crear un mensaje para enviar a Kafka
        order_message = {
            'order_id': order_id,
            'product_name': request.product_name,
            'price': request.price,
            'payment_gateway': request.payment_gateway,
            'card_brand': request.card_brand,
            'bank': request.bank,
            'shipping_address': request.shipping_address,
            'email': request.email,
            'status': 'Procesando'
        }

        try:
            # Publicar el mensaje en Kafka
            self.producer.send('order_topic', order_message)
            self.producer.flush()  # Asegurarse de que el mensaje se envíe inmediatamente

            # Anunciar que el mensaje fue enviado
            logging.info(f"Mensaje de pedido {order_id} enviado a Kafka exitosamente.")

            # Almacenar métricas en Elasticsearch
            self.es.index(index='order_metrics', body={
                'order_id': order_id,
                'status': 'Procesado',
                'price': request.price,
                'payment_gateway': request.payment_gateway,
                'timestamp': time.time()
            })

            # Anunciar que las métricas fueron enviadas
            logging.info(f"Métricas de pedido {order_id} almacenadas en Elasticsearch.")

            # Devolver la respuesta al cliente gRPC
            return pb2.OrderResponse(order_id=order_id, status='Pedido recibido y procesado')

        except Exception as e:
            logging.error(f"Error al procesar el pedido {order_id}: {str(e)}")
            return pb2.OrderResponse(order_id=order_id, status='Error al procesar el pedido')

# Función principal para iniciar el servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_OrderManagementServicer_to_server(OrderManagementService(), server)
    server.add_insecure_port('[::]:50051')
    logging.info("Servidor gRPC escuchando en el puerto 50051...")
    server.start()
    try:
        while True:
            time.sleep(86400)  # Mantener el servidor activo
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
