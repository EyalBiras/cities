import socket
import threading

from GUI.networking import SocketWrapper
from GUI.networking.server_socket import ServerSocket
from db.db import DB


def handle_client(client_socket, db):
    s = ServerSocket(SocketWrapper(client_socket), db)
    while True:
        username, command = s.receive_message()
        if username == "EXIT" and command == "EXIT":
            break
        print(f"details: \n\t{username=}\n\t{command=}")


host = '10.0.0.8'
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
