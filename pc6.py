from pc import Pc
from threading import Thread

pc1 = Pc(6, 6666)

pc1.register()

# implementação de threads para que PC possa se comportar como cliente e servidor
server_thread = Thread(target=pc1.server_function, args=(6666,))
client_thread = Thread(target=pc1.client_function, args=())

server_thread.start()
client_thread.start()
server_thread.join()
client_thread.join()