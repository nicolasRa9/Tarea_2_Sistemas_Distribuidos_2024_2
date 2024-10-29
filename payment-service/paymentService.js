const { Kafka } = require('kafkajs');


// Configuración de Kafka
const kafka = new Kafka({
  clientId: 'payment-service',
  brokers: ['kafka:9092']
});

// Crear un consumidor para el topic "processed_order_topic"
const consumer = kafka.consumer({ groupId: 'payment-group' });

// Crear un productor para el topic "payment_topic"
const producer = kafka.producer();

// Función para simular el procesamiento de pagos
const processPayment = (order) => {
  const isPaymentSuccessful = Math.random() < 0.9; // Simular 90% éxito
  order.payment_status = isPaymentSuccessful ? 'Pago Exitoso' : 'Pago Fallido';
  return order;
};

const run = async () => {
  // Conectar el consumidor y suscribirse al topic 'processed_order_topic'
  await consumer.connect();
  await consumer.subscribe({ topic: 'processed_order_topic', fromBeginning: true });

  // Conectar el productor
  await producer.connect();

  console.log('Microservicio de pagos en ejecución...');

  // Procesar los mensajes
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const order = JSON.parse(message.value.toString());
      console.log(`Recibido pedido procesado para pago: ${JSON.stringify(order)}`);

      // Procesar el pago
      const processedOrder = processPayment(order);
      console.log(`Resultado del pago: ${JSON.stringify(processedOrder)}`);

      // Publicar el resultado del pago en el topic 'payment_topic'
      await producer.send({
        topic: 'payment_topic',
        messages: [{ value: JSON.stringify(processedOrder) }]
      });

      console.log('Resultado del pago enviado al topic "payment_topic".');
    }
  });
};

// Manejo de errores
run().catch(e => console.error(`[Error al procesar el pago] ${e.message}`, e));
