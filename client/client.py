import grpc
import order_management_pb2 as pb2
import order_management_pb2_grpc as pb2_grpc
import os
import random
from faker import Faker

# Dirección del servidor gRPC
server_address = os.getenv('GRPC_SERVER_ADDRESS', 'grpc-server:50051')

fake = Faker()

def registrar_pedido(stub, nombre_producto, precio, pasarela_pago, marca_tarjeta, banco, direccion_envio, email_cliente):
    pedido = pb2.OrderRequest(
        product_name=nombre_producto,
        price=precio,
        payment_gateway=pasarela_pago,
        card_brand=marca_tarjeta,
        bank=banco,
        shipping_address=direccion_envio,
        email=email_cliente
    )
    respuesta = stub.CreateOrder(pedido)
    print(f"Respuesta del servidor: ID del pedido = {respuesta.order_id}, Estado = {respuesta.status}")

def generar_datos_aleatorios():
    nombre_producto = fake.word()
    precio = round(random.uniform(10.0, 1000.0), 2)  # Precio aleatorio entre 10 y 1000
    pasarela_pago = random.choice(["Webpay", "PayPal", "Stripe", "MercadoPago"])
    marca_tarjeta = random.choice(["VISA", "MasterCard", "Amex"])
    banco = random.choice(["Banco ABC", "Banco XYZ", "Banco 123", "Banco DEF"])
    direccion_envio = fake.address()
    email_cliente = fake.email()
    return nombre_producto, precio, pasarela_pago, marca_tarjeta, banco, direccion_envio, email_cliente

def run():
    with grpc.insecure_channel(server_address) as canal:
        stub = pb2_grpc.OrderManagementStub(canal)
        for _ in range(1000):
            nombre_producto, precio, pasarela_pago, marca_tarjeta, banco, direccion_envio, email_cliente = generar_datos_aleatorios()
            registrar_pedido(
                stub,
                nombre_producto=nombre_producto,
                precio=precio,
                pasarela_pago=pasarela_pago,
                marca_tarjeta=marca_tarjeta,
                banco=banco,
                direccion_envio=direccion_envio,
                email_cliente=email_cliente
            )

if __name__ == '__main__':
    run()
