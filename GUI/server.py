import pathlib
import socket

import networking.network_code
from db.db import DB
from GUI.networking.server_socket import ServerSocket
from GUI.networking import SocketWrapper

host = '127.0.0.1'
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)
db = DB()
connections = []
db.get_groups()

print('Initiating clients')
while True:
    for i in range(5):
        conn = sock.accept()
        print("Got connection!")
        s = ServerSocket(SocketWrapper(conn[0]), db)
        db.get_groups()
        while True:
            print(f"details: {s.receive_message()}")
