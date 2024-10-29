const { Kafka } = require('kafkajs');
const axios = require('axios');

// Configurar Kafka y el consumidor
const kafka = new Kafka({
  clientId: 'order-processing-service',
  brokers: ['kafka-broker-1:9092', 'kafka-broker-2:9093']
});

const consumer = kafka.consumer({ groupId: 'order-processing-group' });

// Estados posibles para un pedido
const ORDER_STATES = ["Preparación", "Enviado", "En tránsito", "Entregado"];

// Función para obtener un tiempo de espera aleatorio entre 1 y 30 segundos
function getRandomDelay() {
  return Math.floor(Math.random() * 30000) + 1000;
}

// Función para simular el procesamiento del pedido y cambiar el estado
async function processOrder(order) {
  console.log(`Procesando pedido: ${order.order_id}`);

  // Procesar el pedido en cada estado
  for (const status of ORDER_STATES) {
    // Esperar un tiempo aleatorio antes de cambiar al siguiente estado
    const delay = getRandomDelay();
    console.log(`Esperando ${delay / 1000} segundos para cambiar al estado: ${status}`);
    await new Promise(resolve => setTimeout(resolve, delay));

    console.log(`Pedido ${order.order_id} cambiado al estado: ${status}`);

    // Enviar una actualización del estado al sistema de notificaciones
    try {
      await axios.post('http://notification-service:3000/notify', {
        order_id: order.order_id,
        status: status,
        email: order.email
      });
      console.log(`Notificación enviada para el pedido ${order.order_id} con estado: ${status}`);
    } catch (error) {
      console.error(`Error al enviar notificación para el pedido ${order.order_id}: ${error.message}`);
    }
  }

  console.log(`Pedido ${order.order_id} completado con estado final: Entregado`);
}

// Función principal para consumir mensajes de Kafka
const run = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'order_topic', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const order = JSON.parse(message.value.toString());
      await processOrder(order);
    }
  });
};

run().catch(e => console.error(`[order-processing] Error: ${e.message}`, e));
