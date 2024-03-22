from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

# dicionário para armazenar as chaves públicas
pubKeys = {}

# Função para processar cada requisição dos clientes
def process_request(server_socket):
    while True:
        message, clientAddress = server_socket.recvfrom(2048)
        request = message.decode().split(':')

        print(f'cliente {request[1]} tentando se registrar...')
        print(f'Cliente {request[1]} registrado com sucesso!')

# socket da AC
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("localhost", 7777))

# Thread para processar as requisições
ca_thread = Thread(target=process_request(server_socket), args=(7777,))
ca_thread.start()