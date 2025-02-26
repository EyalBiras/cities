import pathlib
import socket
import time
from email import message_from_file

from GUI.networking.network_code import Codes
from GUI.networking.constants import KILO_BYTE

class SocketWrapper:
    def __init__(self, _socket: socket.socket, encoding: str = "utf-8"):
        self.__socket = _socket
        self.__encoding = encoding

    def send_message_secure(self, message: str) -> None:
        self.__socket.sendall(message.encode(self.__encoding))

    def receive_message_secure(self, size: int = KILO_BYTE) -> str:
        return self.__socket.recv(size).decode(self.__encoding)

    def send_file(self, file_path: pathlib.Path, chunk_size: int = KILO_BYTE) -> Codes:
        self.send_message_secure(file_path.name)  # Send file name
        ack = self.receive_message_secure()  # Wait for receiver to confirm

        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break  # Stop reading when the file is fully sent

                self.__socket.sendall(chunk)  # Send file chunk
                ack = self.receive_message_secure()  # Wait for acknowledgment before sending next chunk

        self.send_message_secure(Codes.FINISHED.value)  # Explicitly send FINISHED
        return self.receive_message_secure()  # Wait for final acknowledgment

    def receive_file(self, save_file: pathlib.Path="", chunk_size: int = KILO_BYTE,
                     max_file_size: int = 300 * KILO_BYTE) -> bool:
        file_name = self.receive_message_secure()  # Receive file name properly
        save_file = pathlib.Path(save_file or file_name)

        self.send_message_secure(Codes.OK.value)  # Acknowledge file name

        save_file.parent.mkdir(parents=True, exist_ok=True)
        with open(save_file, "wb") as f:
            total_size = 0

            while True:
                data_chunk = self.__socket.recv(chunk_size)

                # If the received data is empty, connection might have closed unexpectedly
                if not data_chunk:
                    return False

                try:
                    decoded_message = data_chunk.decode(self.__encoding)
                    if decoded_message == Codes.FINISHED.value:
                        self.send_message_secure(Codes.OK.value)  # Final acknowledgment
                        return True  # Successfully received the file
                except UnicodeDecodeError:
                    pass  # If decoding fails, it's a binary file chunk

                total_size += len(data_chunk)
                if total_size > max_file_size:
                    self.send_message_secure(Codes.FILE_TOO_BIG.value)
                    return False  # File too large, abort

                f.write(data_chunk)  # Write file chunk
                self.send_message_secure(Codes.OK.value)  # Acknowledge received chunk
