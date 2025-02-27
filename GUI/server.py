import socket
import threading
import pathlib

import networking.network_code
from db.db import DB
from GUI.networking.server_socket import ServerSocket
from GUI.networking import SocketWrapper

def handle_client(client_socket, db):
    s = ServerSocket(SocketWrapper(client_socket), db)
    while True:
        message = s.receive_message()
        if message is None:
            break
        print(f"details: {message}")

host = '127.0.0.1'
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(5)

db = DB()

print('Initiating clients')
while True:
    client_socket, addr = sock.accept()
    print(f"Got connection from {addr}!")
    client_thread = threading.Thread(target=handle_client, args=(client_socket, db))
    client_thread.daemon = True
    client_thread.start()