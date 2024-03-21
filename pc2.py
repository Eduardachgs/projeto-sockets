from pc import Pc
from threading import Thread

pc2 = Pc(2, 2222)

pc2.register()

server_thread = Thread(target=pc2.server_function, args=(2222,))
client_thread = Thread(target=pc2.client_function, args=())

server_thread.start()
client_thread.start()
server_thread.join()
client_thread.join()