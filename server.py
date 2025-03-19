import grpc
from concurrent import futures
import threading
import chat_pb2
import chat_pb2_grpc

class ChatServicer(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        self.clients = []  # Lista para armazenar os streams dos clientes
        self.lock = threading.Lock()  # Lock para garantir thread safety

    def SendMessage(self, request_iterator, context):
        # Cria um stream para enviar mensagens para este cliente
        def message_generator():
            while True:
                with self.lock:
                    for client in self.clients:
                        if client["stream"] == request_iterator:
                            for message in client["messages"]:
                                yield message
                            client["messages"].clear()

        # Adiciona o cliente à lista de clientes conectados
        with self.lock:
            self.clients.append({
                "stream": request_iterator,
                "messages": []
            })

        # Recebe mensagens do cliente
        for message in request_iterator:
            print(f"[{message.user}] {message.message}")
            # Retransmite a mensagem para todos os clientes conectados
            with self.lock:
                for client in self.clients:
                    if client["stream"] != request_iterator:  # Não envia a mensagem de volta para o remetente
                        client["messages"].append(message)

        # Retorna o stream de mensagens para o cliente
        return message_generator()

def start_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Servidor rodando na porta {port}...")
    server.wait_for_termination()

if __name__ == "__main__":
    port = 50051
    start_server(port)