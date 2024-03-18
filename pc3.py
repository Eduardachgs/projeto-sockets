from pc import Pc
from threading import Thread

pc3 = Pc(3333)

pc3.register()

# implementação de threads para que PC possa se comportar como cliente e servidor
server_thread = Thread(target=pc3.server_function, args=(3333,))
client_thread = Thread(target=pc3.client_function, args=())

server_thread.start()
client_thread.start()
server_thread.join()
client_thread.join()