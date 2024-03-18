from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
import os


def generate_keys():
    parameters = dh.generate_parameters(generator=2, key_size=1024)
    # Gera a chave privada
    private_key = parameters.generate_private_key()
    # Gera a chave pública
    public_key = private_key.public_key()
    return private_key, public_key

def generate_symetric(private_key, public_key):
    # Gera a chave compartilhada
    shared_key = private_key.exchange(public_key)
    derived_key = HKDF( 
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)
    return derived_key

def encrypt_decrypt(derived_key):
    # Gera um nonce
    nonce = os.urandom(16)
    # Cria o objeto cipher
    cipher = Cipher(algorithms.AES(derived_key), mode=modes.CTR(nonce))
    return cipher

"""
            parameters = dh.generate_parameters(generator=2, key_size=2048)
            server_private_key = parameters.generate_private_key()
            server_public_key = server_private_key.public_key()
            shared_key = server_private_key.exchange(request)
            symKeys[clientAddress[1]] = HKDF(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=None,
                    info=b'handshake data',
                ).derive(shared_key)
            nonce = secrets.token_bytes(16)
            privKey = new_keys(clientAddress[1])

            # Encripta a chave privada com a chave simétrica
            cipher_server = Cipher(algorithms.AES(symKeys[clientAddress[1]]), mode=modes.CTR(nonce))
            encryptor = cipher_server.encryptor()
            ciphertext = encryptor.update(str(privKey).encode()) + encryptor.finalize()
            nonce = encryptor.update(str(nonce).encode()) + encryptor.finalize()
            ans = ciphertext, server_public_key
            server_socket.sendto(ans, clientAddress)
            
            # priv_num = randint(1, 1000) 
            # x = (3 ** priv_num) % 17 
            # symKeys[clientAddress[1]] = int(request)**priv_num % 17
            # privKey = new_keys(clientAddress[1])

            # # Encripta a chave privada com a chave simétrica
            # cipher = AES.new(symKeys[clientAddress[1]].to_bytes(16, 'big'), AES.MODE_EAX)
            # ciphertext, tag = cipher.encrypt_and_digest(str(privKey))

            # ans = f'{x},{ciphertext},{tag}'
            # server_socket.sendto(ans.encode(), clientAddress)
"""

"""
        socket_client = socket(AF_INET, SOCK_DGRAM)
        server_address = ('localhost', 7777) # endereço e porta da autoridade

        # Diffie-Hellman
        parameters = dh.generate_parameters(generator=2, key_size=2048)
        peer_private_key = parameters.generate_private_key()
        peer_public_key = peer_private_key.public_key()

        socket_client.sendto(f'{peer_public_key}'.encode(), server_address)
        ans, sAddress = socket_client.recvfrom(2048)
        ans = ans.decode()
        ans = ans.split(',')
        shared_key = peer_private_key.exchange(int(ans[0]))
        self.simetric_keys[sAddress[1]] = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)
        nonce = secrets.token_bytes(16)
        cipher = Cipher(algorithms.AES(self.simetric_keys[sAddress[1]]), mode=modes.CTR(nonce))
        decryptor = cipher.decryptor()
        self.privKey = decryptor.update(ans[0].encode()) + decryptor.finalize()

        # priv_num = randint(1, 1000) # número aleatório para gerar a chave simétrica
        # x = (3 ** priv_num) % 17 # cálculo da chave simétrica pública

        # socket_client.sendto(f'{x}'.encode(), server_address)
        # ans, sAddress = socket_client.recvfrom(2048)
        # ans = ans.decode()
        # ans = ans.split(',')

        # self.symeys[sAddress[1]] = ans[0]**priv_num % 17 # cálculo da chave simétrica privada
        # cipher = AES.new(self.simetric_keys[sAddress[1]], AES.MODE_EAX)
        # self.privKey = cipher.decrypt_and_verify(ans[1], ans[2]) # descriptografa a chave privada
"""