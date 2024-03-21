from roteamento import Roteamento
from socket import socket, AF_INET, SOCK_DGRAM
import rsa
import pickle

roteamento = Roteamento()
class Pc:
    def __init__(self, pc, porta):
        self.pc = pc
        self.porta = porta
        self.simetric_keys = {} # dicionário para armazenar as chaves simétricas
        self.privKey = None
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)

    # função para que o nó possa se registrar na autoridade
    def register(self):
        server_address = ('localhost', 7777) # endereço e porta da autoridade
        request = 'register'
        self.client_socket.sendto(request.encode(), server_address)
        
        print('Registrando o nó na autoridade...')
        ans, sAddress = self.client_socket.recvfrom(2048)
        # ans = pickle.loads(ans)
        # self.privKey = rsa.decrypt(ans, privkey)
        
        print(f'Nó registrado com sucesso!')


    def server_function(self, porta):
        # associar socket a endereço e porta
        self.server_socket.bind(("localhost", porta))

        # loop para receber mensagens dos outros PCs
        while True:
            message, clientAddress = self.server_socket.recvfrom(2048) # recebe até 2048 bytes
            request = message.decode()

            if request[0:4] == 'RRRR':
                _, pc_origem, pc_destino, msg = request.split(':')

                if self.pc == int(pc_destino):
                    print(f"A mensagem recebida foi: {msg}")
                
                else: 
                    pc_origem = self.pc
                    prox_pc = roteamento.enviar_mensagens(pc_origem, int(pc_destino))
                    destino = ('localhost', int(str(prox_pc)*4))
                    self.client_socket.sendto(request.encode(), destino)
            else:
                print()
                print(f"A mensagem recebida de {clientAddress} foi: {request}")

                ans = f"Olá, cliente {clientAddress}"
                self.server_socket.sendto(ans.encode(), clientAddress)

    def client_function(self):
        iniciar = input('Digite enter para iniciar a comunicação entre os PCs')
        
        # primeiro loop para enviar mensagens para todos os PCs
        for i in range(6):
            destino = int(str(i+1)*4)
            if destino == self.porta:
                continue

            server_address = ('localhost', destino)
            if (self.pc == 1 and (i+1) == 6) or (self.pc == 6 and (i+1) == 1):
                for j in range(5):
                    message = f"PC{self.pc} aqui! Mensagem {j+1} para o PC {i+1}"

                    # enviamos a mensagem pelo socket criado
                    self.client_socket.sendto(message.encode(), server_address)

                    # recebendo as respostas do servidor
                    ans, sAddress = self.client_socket.recvfrom(2048)
                    ans = ans.decode()

                    print(f"A resposta recebida foi: {ans}")

            elif (i+1) == self.pc+1 or (i+1) == self.pc-1:
            # segundo loop para enviar 5 mensagens para cada PC
                for j in range(5):
                    message = f"PC{str(self.porta)[0]} aqui! Mensagem {j+1} para o PC {i+1}"

                    # enviamos a mensagem pelo socket criado
                    self.client_socket.sendto(message.encode(), server_address)

                    # recebendo as respostas do servidor
                    ans, sAddress = self.client_socket.recvfrom(2048)
                    ans = ans.decode()

                    print(f"A resposta recebida foi: {ans}")

            else:
                for j in range(5):
                    prox_pc = roteamento.enviar_mensagens(self.pc, i+1)
                    destino = ('localhost', int(str(prox_pc)*4))

                    message = f'RRRR:{self.pc}:{i+1}:PC{self.pc} aqui! Mensagem {j+1} roteada para o PC {i+1}'
                    self.client_socket.sendto(message.encode(), destino)

            #socket_client.close()


