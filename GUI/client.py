import pathlib
import socket

from networking.socket_wrapper import SocketWrapper

host = '127.0.0.1'
port = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connecting with Server
sock.connect((host, port))
s = SocketWrapper(sock)
s.send_file(pathlib.Path("a.txt"))