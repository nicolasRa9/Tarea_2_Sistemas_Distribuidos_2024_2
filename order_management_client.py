import grpc
import order_management_pb2_grpc as pb2_grpc
import order_management_pb2 as pb2

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.OrderManagementStub(channel)

        # Crear un pedido
        order = pb2.OrderRequest(
            product_name="Laptop",
            price=1500.00,
            payment_gateway="Webpay",
            card_brand="VISA",
            bank="BancoEstado",
            shipping_address="Región de Coquimbo, Chile",
            email="cliente@correo.com"
        )

        # Llamar al método remoto CreateOrder
        response = stub.CreateOrder(order)
        print(f"Pedido realizado: {response.order_id}, Estado: {response.status}")

if __name__ == '__main__':
    run()
