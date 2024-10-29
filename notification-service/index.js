const express = require('express');
const nodemailer = require('nodemailer');

const app = express();
app.use(express.json()); // Middleware para manejar JSON

// Configuración de transporte para nodemailer
const transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com', // Cambia a tu servidor SMTP
    port: 587,
    secure: false, // true para el puerto 465, false para otros puertos
    auth: {
        user: 'sistema.dtest2@gmail.com', // tu correo electrónico
        pass: 'yozu gsym titv zvsc' // tu contraseña
    }
});

// Endpoint para recibir notificaciones
app.post('/notify', async (req, res) => {
    const { orderId, status, email } = req.body;

    // Configurar el contenido del correo electrónico
    const mailOptions = {
        from: 'sistema.dtest2@gmail.com', // Dirección de correo del remitente
        to: email, // Dirección de correo del destinatario
        subject: 'Actualización de Pedido',
        text: `Su pedido con ID ${orderId} ha cambiado al estado: ${status}`
    };

    try {
        // Enviar el correo electrónico
        await transporter.sendMail(mailOptions);
        console.log(`Correo de notificación enviado a ${email} para el pedido ${orderId}`);
        res.status(200).json({ message: 'Notificación enviada con éxito' });
    } catch (error) {
        console.error(`Error al enviar el correo: ${error.message}`);
        res.status(500).json({ message: 'Error al enviar notificación' });
    }
});

// Iniciar el servidor en el puerto 3000
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servicio de notificación ejecutándose en el puerto ${PORT}`);
});
