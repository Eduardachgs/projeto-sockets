
from socket import socket, AF_INET, SOCK_DGRAM


class Pc:
    def __init__(self, porta, destino):
        self.porta = porta
        self.destino = destino
        self.simetric_keys = {} # dicionário para armazenar as chaves simétricas
        self.privKey = None

    # função para que o nó possa se registrar na autoridade
    def register(self):
        socket_client = socket(AF_INET, SOCK_DGRAM)
        server_address = ('localhost', 7777) # endereço e porta da autoridade
        message = f"register,{self.porta}"
        socket_client.sendto(message.encode(), server_address)
        
        print('Registrando o nó na autoridade...')
        ans, sAddress = socket_client.recvfrom(2048)
        ans = ans.decode()
        print(f'Mensagem da autoridade: {ans}')


    def server_function(self, porta):
        # criar socket UDP
        server_socket = socket(AF_INET, SOCK_DGRAM)
        # associar socket a endereço e porta
        server_socket.bind(("localhost", porta))

        # loop para receber n mensagens de um cliente
        for i in range(3):
            message, clientAddress = server_socket.recvfrom(2048) # recebe até 2048 bytes
            request = message.decode()
            print()
            print(f"A mensagem recebida de {clientAddress} foi {request}")

            ans = f"Olá, cliente {clientAddress}"
            server_socket.sendto(ans.encode(), clientAddress)

    def client_function(self):
        while True:
            destino = int(input("Digite o número do cliente com o qual quer se comunicar: "))
            # criar socket UDP
            socket_client = socket(AF_INET, SOCK_DGRAM)
            server_address = ('localhost', destino)

            message = input(">>>")

            # enviamos a mensagem pelo socket criado
            socket_client.sendto(message.encode(), server_address)

            # recebendo as respostas do servidor
            ans, sAddress = socket_client.recvfrom(2048)
            ans = ans.decode()

            print(f"A resposta recebida foi: {ans}")

            socket_client.close()



