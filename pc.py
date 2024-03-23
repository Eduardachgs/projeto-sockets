from roteamento import Roteamento
from socket import socket, AF_INET, SOCK_DGRAM

roteamento = Roteamento()
class Pc:
    def __init__(self, pc, porta):
        self.pc = pc
        self.porta = porta
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)

    # Função para que o nó possa se registrar na autoridade assim que o programa for instanciado
    def register(self):
        server_address = ('localhost', 7777) # endereço e porta da autoridade
        request = f'register:{self.pc}'
        self.client_socket.sendto(request.encode(), server_address)
        
        print('Registrando o nó na autoridade...')
        print('Nó registrado com sucesso!')

    # Função para receber mensagens de outros PCs
    def server_function(self, porta):
        # associar socket a endereço e porta
        self.server_socket.bind(("localhost", porta))

        # Loop para receber mensagens dos outros PCs
        while True:
            message, clientAddress = self.server_socket.recvfrom(2048)
            request = message.decode()

            # Se a mensagem iniciar com a tag RRRR ela foi roteada
            if request[0:4] == 'RRRR' or request[0:4] == 'BBBB':
                _, pc_origem, pc_destino, msg = request.split(':')

                # Verifica se a mensagem é para o PC atual
                if self.pc == int(pc_destino):
                    if request[0:4] == 'BBBB':
                        ans = f'{self.pc} recebeu a mensagem roteada'
                        _, pc_origem, pc_destino, msg = request.split(':')
                        print(f"A mensagem recebida foi: {msg}")
                        ans = f'RRRR:{self.pc}:{int(msg[2])}:PC{self.pc} recebeu a mensagem broadcast'
                        destino = roteamento.enviar_mensagens(self.pc, int(msg[2]))
                        destino = ('localhost', int(str(destino)*4))
                        self.server_socket.sendto(ans.encode(), destino)

                    else:
                        print(f"A mensagem recebida foi: {msg}")
                
                # Se não for, roteia a mensagem para o próximo PC
                else: 
                    pc_origem = self.pc
                    prox_pc = roteamento.enviar_mensagens(pc_origem, int(pc_destino))
                    destino = ('localhost', int(str(prox_pc)*4))
                    self.client_socket.sendto(request.encode(), destino)

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

            destino = ('localhost', destino)
            # Condicionais para determinar o destino adequado dos pacotes
            if (self.pc == 1 and (i+1) == 6) or (self.pc == 6 and (i+1) == 1):
                # segundo loop para enviar 5 mensagens para cada PC
                for j in range(5):
                    message = f"PC{self.pc} aqui! Mensagem {j+1} para o PC {i+1}"
                    self.client_socket.sendto(message.encode(), destino)

            elif (i+1) == self.pc+1 or (i+1) == self.pc-1:
                for j in range(5):
                    message = f"PC{str(self.porta)[0]} aqui! Mensagem {j+1} para o PC {i+1}"

                    # enviamos a mensagem pelo socket criado
                    self.client_socket.sendto(message.encode(), destino)
                

            else:
                prox_pc = roteamento.enviar_mensagens(self.pc, i+1)
                destino = ('localhost', int(str(prox_pc)*4))
                for j in range(5):
                    # Usa a função de roteamento para determinar o próximo PC
                    message = f'RRRR:{self.pc}:{i+1}:PC{self.pc} aqui! Mensagem {j+1} roteada para o PC {i+1}'
                    self.client_socket.sendto(message.encode(), destino)
                
            mensagem_broadcast = f"BBBB:{self.pc}:{i+1}:PC{self.pc} aqui! Mensagem broadcast para todos os PCs"
            self.client_socket.sendto(mensagem_broadcast.encode(), destino)
        

