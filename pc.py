from roteamento import Roteamento
from socket import socket, AF_INET, SOCK_DGRAM
import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

roteamento = Roteamento()
class Pc:
    def __init__(self, pc, porta):
        self.pc = pc
        self.porta = porta
        self.privKey = None
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)

    # função para que o nó possa se registrar na autoridade
    def register(self):
        server_address = ('localhost', 7777) # endereço e porta da autoridade
        request = f'{self.pc}:register'
        self.client_socket.sendto(request.encode(), server_address)
        
        print('Registrando o nó na autoridade...')
        ans, sAddress = self.client_socket.recvfrom(2048)
        self.privKey = rsa.PrivateKey.load_pkcs1(ans)
        
        print(f'Nó registrado com sucesso!')


    def server_function(self, porta):
        # associar socket a endereço e porta
        self.server_socket.bind(("localhost", porta))

        # loop para receber mensagens dos outros PCs
        while True:
            message, clientAddress = self.server_socket.recvfrom(2048) # recebe até 2048 bytes
            try:
                request = message.decode()
            except:
                request = message
            
            if request[:-1] == 'keys':
                print()
                # ARRUMAR ISSO AQUI
                key, clientAddress = self.server_socket.recvfrom(2048)
                nonce, clientAddress = self.server_socket.recvfrom(2048)
                key = rsa.decrypt(key, self.privKey)
                nonce = rsa.decrypt(nonce, self.privKey)
                cipher = AES.new(key, AES.MODE_EAX, nonce)
                print(f'Mensagens de PC{request[-1]}:')
                for i in range(5):
                    if i > 0:
                        key, clientAddress = self.server_socket.recvfrom(2048)
                        nonce, clientAddress = self.server_socket.recvfrom(2048)
                        key = rsa.decrypt(key, self.privKey)
                        nonce = rsa.decrypt(nonce, self.privKey)
                        cipher = AES.new(key, AES.MODE_EAX, nonce)
                    message, clientAddress = self.server_socket.recvfrom(2048)
                    tag = message[:16]
                    message = message[16:]
                    message = cipher.decrypt_and_verify(message, tag).decode('utf-8')
                    print(f"A mensagem recebida foi: {message}")


            elif request[0:4] == 'RRRR':
                _, pc_origem, pc_destino, original = request.split(':')

                if self.pc == int(pc_destino):
                    # adicionar a descriptografia da mensagem
                    print(f'Mensagens de PC{original}:')
                    key, clientAddress = self.server_socket.recvfrom(2048)
                    nonce, clientAddress = self.server_socket.recvfrom(2048)
                    key = rsa.decrypt(key, self.privKey)
                    nonce = rsa.decrypt(nonce, self.privKey)
                    cipher = AES.new(key, AES.MODE_EAX, nonce)
                    msg, clientAddress = self.server_socket.recvfrom(2048)
                    tag = msg[:16]
                    msg = msg[16:]
                    msg = cipher.decrypt_and_verify(msg, tag).decode('utf-8')
                    print(f"A mensagem recebida foi: {msg}")
                
                else: 
                    pc_origem = self.pc
                    prox_pc = roteamento.enviar_mensagens(pc_origem, int(pc_destino))
                    destino = ('localhost', int(str(prox_pc)*4))
                    self.client_socket.sendto(request.encode(), destino)
                    for i in range(3):
                        k, clientAddress = self.server_socket.recvfrom(2048)
                        self.client_socket.sendto(k, destino)

            # else:
            #     print()
            #     print(f"A mensagem recebida de {clientAddress} foi: {request}")

            #     ans = f"Olá, cliente {clientAddress}"
            #     self.server_socket.sendto(ans.encode(), clientAddress)

    def client_function(self):
        iniciar = input('Digite enter para iniciar a comunicação entre os PCs')
        
        # primeiro loop para enviar mensagens para todos os PCs
        for i in range(6):
            destino = int(str(i+1)*4)
            if destino == self.porta:
                continue
            
            server_address = ('localhost', 7777)
            request = f'{self.pc}:get_pubkey:{destino}'
            self.client_socket.sendto(request.encode(), server_address)
            ans, sAddress = self.client_socket.recvfrom(2048)
            pubKey_destino = rsa.PublicKey.load_pkcs1(ans)



            server_address = ('localhost', destino)
            if (self.pc == 1 and (i+1) == 6) or (self.pc == 6 and (i+1) == 1):


                mensagem = f'keys{self.pc}'
                self.client_socket.sendto(mensagem.encode(), server_address)
                for j in range(5):
                    key = get_random_bytes(16)
                    cipher = AES.new(key, AES.MODE_EAX)
                    nonce = cipher.nonce
                    key = rsa.encrypt(key, pubKey_destino)
                    nonce = rsa.encrypt(nonce, pubKey_destino)
                    self.client_socket.sendto(key, server_address)
                    self.client_socket.sendto(nonce, server_address)
                    message = b"Mensagem..."
                    ciphertext, tag = cipher.encrypt_and_digest(message)
                    message = tag+ciphertext
                    # enviamos a mensagem pelo socket criado
                    self.client_socket.sendto(message, server_address)

            elif (i+1) == self.pc+1 or (i+1) == self.pc-1:
            # segundo loop para enviar 5 mensagens para cada PC
                mensagem = f'keys{self.pc}'
                self.client_socket.sendto(mensagem.encode(), server_address)
                for j in range(5):
                    key = get_random_bytes(16)
                    cipher = AES.new(key, AES.MODE_EAX)
                    nonce = cipher.nonce
                    key = rsa.encrypt(key, pubKey_destino)
                    nonce = rsa.encrypt(nonce, pubKey_destino)
                    self.client_socket.sendto(key, server_address)
                    self.client_socket.sendto(nonce, server_address)
                    message = b"Mensagem..."
                    ciphertext, tag = cipher.encrypt_and_digest(message)
                    message = tag+ciphertext
                    # enviamos a mensagem pelo socket criado
                    self.client_socket.sendto(message, server_address)

            else:
                for j in range(5):
                    prox_pc = roteamento.enviar_mensagens(self.pc, i+1)
                    destino = ('localhost', int(str(prox_pc)*4))

                    message = f'RRRR:{self.pc}:{i+1}:{self.pc}'
                    self.client_socket.sendto(message.encode(), destino)

                    key = get_random_bytes(16)
                    cipher = AES.new(key, AES.MODE_EAX)
                    nonce = cipher.nonce
                    key = rsa.encrypt(key, pubKey_destino)
                    nonce = rsa.encrypt(nonce, pubKey_destino)
                    self.client_socket.sendto(key, server_address)
                    self.client_socket.sendto(nonce, server_address)
                    message = b"Mensagem..."
                    ciphertext, tag = cipher.encrypt_and_digest(message)
                    message = tag+ciphertext
                    # enviamos a mensagem pelo socket criado
                    self.client_socket.sendto(message, server_address)


            #socket_client.close()