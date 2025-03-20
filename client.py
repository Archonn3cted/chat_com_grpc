import grpc
import chat_pb2
import chat_pb2_grpc
import threading

def receive_messages(stub):
    # Recebe mensagens do servidor
    for message in stub.SendMessage(iter(())):
        print(f"[{message.user}] {message.message}")

def send_messages(stub, user):
    # Envia mensagens para o servidor
    while True:
        message = input()
        stub.SendMessage(iter([chat_pb2.ChatMessage(user=user, message=message)]))

def start_client(server_address, user):
    channel = grpc.insecure_channel(server_address)
    stub = chat_pb2_grpc.ChatStub(channel)

    # Thread para receber mensagens
    threading.Thread(target=receive_messages, args=(stub,), daemon=True).start()

    # Envia mensagens
    send_messages(stub, user)

if __name__ == "__main__":
    server_address = "localhost:50051"
    user = input("Digite seu nome: ")
    start_client(server_address, user)