import rsa 
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import pickle

# dicionário para armazenar as chaves públicas
pubKeys = {}
symKeys = {}

def register(pc):
    pass

# Função para processar cada requisição dos clientes
def process_request(server_socket):
    while True:
        message, clientAddress = server_socket.recvfrom(2048)
        request = message.decode()

        # Verifica se o nó já está registrado
        if clientAddress[1] not in pubKeys.keys():
            print(f'cliente {clientAddress} tentando se registrar...')

            #ciphertext = rsa.encrypt(privkey, client_pubkey) # usa chave pública do criente para criptografar a chave privada
            ciphertext = 'oi'.encode()
            server_socket.sendto(ciphertext, clientAddress)
            pubKeys[clientAddress[1]] = clientAddress

            print(f'Cliente {clientAddress} registrado com sucesso!')
        else:    
            print(f'A mensagem recebida de {clientAddress} foi {request}')

            ans = f'Olá, cliente {clientAddress}'
            server_socket.sendto(ans.encode(), clientAddress)

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("localhost", 7777))


ca_thread = Thread(target=process_request(server_socket), args=(7777,))
ca_thread.start()