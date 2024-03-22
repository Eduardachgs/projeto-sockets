import rsa 
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

# dicionário para armazenar as chaves públicas
pubKeys = {}
symKeys = {}

# Função para processar cada requisição dos clientes
def process_request(server_socket):
    while True:
        message, clientAddress = server_socket.recvfrom(2048)
        request = message.decode()
        request = request.split(':')

        # Verifica se o nó já está registrado
        if request[1] == 'register':
            print(f'PC {request[0]} tentando se registrar...')
            pubkey, privkey = rsa.newkeys(512) # gera chaves pública e privada
            privkey = privkey.save_pkcs1()
            server_socket.sendto(privkey, clientAddress)

            pubKeys[request[0]] = pubkey

            print(f'PC {request[0]} registrado com sucesso!')
        else:
            print(f'Pc {request[0]} solicitando chave pública de PC{request[2]}')    
            pubkey = pubKeys[request[2][0]]
            pubkey = pubkey.save_pkcs1()
            server_socket.sendto(pubkey, clientAddress)
            print('Chave enviada com sucesso!')

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("localhost", 7777))


ca_thread = Thread(target=process_request(server_socket), args=(7777,))
ca_thread.start()