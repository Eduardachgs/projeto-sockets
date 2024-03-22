from pc import Pc
from threading import Thread

pc1 = Pc(5, 5555)

pc1.register()

server_thread = Thread(target=pc1.server_function, args=(5555,))
client_thread = Thread(target=pc1.client_function, args=())

server_thread.start()
client_thread.start()
server_thread.join()
client_thread.join()