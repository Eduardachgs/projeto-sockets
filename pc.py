from roteamento import Roteamento
from socket import socket, AF_INET, SOCK_DGRAM

roteamento = Roteamento()
class Pc:
    def __init__(self, pc, porta):
        self.pc = pc
        self.porta = porta
        self.simetric_keys = {} 
        self.privKey = None
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)

    # Função para que o nó possa se registrar na autoridade assim que o programa for instanciado
    def register(self):
        server_address = ('localhost', 7777) # endereço e porta da autoridade
        request = f'register:{self.pc}'
        self.client_socket.sendto(request.encode(), server_address)
        
        print('Registrando o nó na autoridade...')
        print(f'Nó registrado com sucesso!')

    # Função para receber mensagens de outros PCs
    def server_function(self, porta):
        # associar socket a endereço e porta
        self.server_socket.bind(("localhost", porta))

        # Loop para receber mensagens dos outros PCs
        while True:
            message, clientAddress = self.server_socket.recvfrom(2048)
            request = message.decode()

            # Se a mensagem iniciar com a tag RRRR ela foi roteada
            if request[0:4] == 'RRRR':
                _, pc_origem, pc_destino, msg = request.split(':')

                # Verifica se a mensagem é para o PC atual
                if self.pc == int(pc_destino):
                    print(f"A mensagem recebida foi: {msg}")
                
                # Se não for, roteia a mensagem para o próximo PC
                else: 
                    pc_origem = self.pc
                    prox_pc = roteamento.enviar_mensagens(pc_origem, int(pc_destino))
                    destino = ('localhost', int(str(prox_pc)*4))
                    self.client_socket.sendto(request.encode(), destino)

            # Tag BBBB indica broadcast
            elif request[0:4] == 'BBBB':
                _, msg = request.split(':')
                print(f"A mensagem recebida foi: {msg}")
                ans = f'{self.pc} recebeu a mensagem broadcast'
                self.server_socket.sendto(ans.encode(), clientAddress)

            # Se não for roteada, a mensagem é para o PC atual
            else:
                print(f"A mensagem recebida foi: {request}")

    # Função para enviar mensagens para outros PCs
    def client_function(self):
        iniciar = input('Digite enter para iniciar a comunicação entre os PCs\n')
        
        # primeiro loop para enviar mensagens para todos os PCs
        for i in range(6):
            destino = int(str(i+1)*4)
            if destino == self.porta:
                continue

            server_address = ('localhost', destino)
            # Condicionais para determinar o destino adequado dos pacotes
            if (self.pc == 1 and (i+1) == 6) or (self.pc == 6 and (i+1) == 1):
                # segundo loop para enviar 5 mensagens para cada PC
                for j in range(5):
                    message = f"PC{self.pc} aqui! Mensagem {j+1} para o PC {i+1}"
                    self.client_socket.sendto(message.encode(), server_address)

            elif (i+1) == self.pc+1 or (i+1) == self.pc-1:
                for j in range(5):
                    message = f"PC{str(self.porta)[0]} aqui! Mensagem {j+1} para o PC {i+1}"

                    # enviamos a mensagem pelo socket criado
                    self.client_socket.sendto(message.encode(), server_address)

            else:
                for j in range(5):
                    # Usa a função de roteamento para determinar o próximo PC
                    prox_pc = roteamento.enviar_mensagens(self.pc, i+1)
                    destino = ('localhost', int(str(prox_pc)*4))
                    message = f'RRRR:{self.pc}:{i+1}:PC{self.pc} aqui! Mensagem {j+1} roteada para o PC {i+1}'
                    self.client_socket.sendto(message.encode(), destino)
        
        mensagem_broadcast = f"BBBB:PC{self.pc} aqui! Mensagem broadcast para todos os PCs"
        # Loop para enviar mensagem broadcast para todos os PCs
        for i in range(6):
            if self.pc == i+1:
                continue
            destino = ('localhost', int(str(i+1)*4))
            self.client_socket.sendto(mensagem_broadcast.encode(), destino)
            ans, sAddress = self.client_socket.recvfrom(2048)
            ans = ans.decode()
            print(ans)


