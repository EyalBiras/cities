import pathlib
import socket
import time
from pprint import pformat

from GUI.networking import Command
from GUI.networking.network_code import Codes
from GUI.networking.constants import KILO_BYTE, INVALID_USERNAME_OR_PASSWORD
from GUI.networking.socket_wrapper import SocketWrapper
from GUI.db.db import DB
DEVELOPMENT_CODE_DIR = "development_code"
ONE_MEGABYTE = 1048576
MAX_SIZE = ONE_MEGABYTE
MAX_SIZE_STR = "1mb"
MAX_AMOUNT_OF_FILES = 40
file = pathlib.Path(__file__)
RESULTS_FILE = file.parent.parent.parent / "results.json"

BASE_PATH = file.parent.parent.parent / "groups"
print(BASE_PATH)
GAMES_DIRECTORY = file.parent.parent.parent / "games"


def get_group_directory(group: str) -> pathlib.Path:
    return BASE_PATH / pathlib.Path(group)


class ServerSocket:
    def __init__(self, server_socket: SocketWrapper, db: DB):
        self.__server_socket = server_socket
        self.db = db

    def receive_message(self, size: int = KILO_BYTE) -> tuple[str, str]:
        x = self.__server_socket.receive_message_secure(size).split(",")
        print(f"{x=}")
        username, password, command, details = x
        print(f"{username=}, {password=}, {command=}, {details=}")
        verification_code = Codes.OK.value
        if not self.db.validate_user(username, password):
            verification_code = Codes.INVALID_USERNAME_OR_PASSWORD.value
            message = "NO"
            return_code = Codes.INVALID_USERNAME_OR_PASSWORD.value
            self.__server_socket.send_message_secure(f"{verification_code}|{message}|{return_code}")
            self.__server_socket.receive_message_secure()
            return INVALID_USERNAME_OR_PASSWORD, ""

        message = ""
        return_code = Codes.OK
        if command == Command.GET_GROUPS.value:
            groups = self.db.get_groups()
            message = f"({str(groups[0])}"
            for group in groups[1:]:
                message += f"),({str(group)}"
            message += ")"
            return_code = Codes.OK
        if command == Command.JOIN_GROUP.value:
            if self.db.ask_for_join_request(username, details):
                return_code = Codes.OK

            else:
                return_code = Codes.FAILED_TO_JOIN

        if command == Command.LEAVE_GROUP.value:
            if self.db.is_in_group(username):
                self.db.leave_group(username)
                return_code = Codes.OK
            else:
                return_code = Codes.NOT_IN_GROUP

        if command == Command.IS_IN_GROUP.value:
            if self.db.is_in_group(username):
                print("In group")
                message = Codes.HAS_GROUP.value
                return_code = Codes.OK
            else:
                message = Codes.NOT_IN_GROUP.value
                return_code = Codes.NOT_IN_GROUP

        if command == Command.CREATE_GROUP.value:
            if self.db.is_in_group(username):
                message = Codes.HAS_GROUP.value
                return_code = Codes.OK
            else:
                self.db.create_group(username, details)
                return_code = Codes.OK

        if command == Command.IS_GROUP_OWNER.value:
            if self.db.is_group_owner(username):
                message = Codes.GROUP_OWNER.value
                return_code = Codes.OK
            else:
                message = Codes.NOT_GROUP_OWNER.value
                return_code = Codes.NOT_GROUP_OWNER

        if command == Command.GET_GROUP_MEMBERS.value:
            if self.db.is_in_group(username):
                group = self.db.get_group(username)
                message = f"Owner: {group.owner}\n"
                for member in group.users:
                    if member != group.owner:
                        message += f"{member}\n"
                return_code = Codes.OK
            else:
                return_code = Codes.NOT_IN_GROUP
        if command == Command.GET_JOIN_REQUESTS.value:
            if self.db.is_in_group(username):
                join_requests = self.db.get_join_requests(username)
                message = f"{join_requests[0]}"
                for request in join_requests[1:]:
                    message += f",{request}"
                return_code = Codes.OK

            else:
                return_code = Codes.NOT_IN_GROUP
        if command == Command.ACCEPT_JOIN_REQUEST.value:
            if self.db.is_asking_for_join_request(details, username):
                self.db.accept_join_request(username, details)
                message = Codes.ACCEPTED_JOIN_REQUEST.value
                return_code = Codes.OK
            else:
                return_code = Codes.NOT_IN_GROUP
        if command == Command.GET_FILES:
            if self.db.is_in_group(username):
                group = self.db.get_group(username)
                group_directory = get_group_directory(group.name) / DEVELOPMENT_CODE_DIR
                if group_directory.exists():
                    for file_path in group_directory.rglob("*"):
                        message += f"{pathlib.Path(file_path).name},"
                    message = message[:-1]
        if command == Command.DOWNLOAD_RESULTS_INFO:
            group, enemy = details.split("|")
            self.__server_socket.send_message_secure(
                f"{verification_code}|{message}|{return_code.value}")
            for f in GAMES_DIRECTORY.glob("*"):
                file = pathlib.Path(f)
                print(file.name)
                if group and enemy in file.name:
                    print("hi")
                    return_code = Codes.OK
                    self.__server_socket.send_file(file)
                    self.__server_socket.receive_message_secure()
            else:
                return_code = Codes.NOT_IN_GROUP
        if command == Command.GET_USER_GROUP:
            if self.db.is_in_group(username):
                group = self.db.get_group(username)
                message = group.name
                return_code = Codes.OK
            else:
                return_code = Codes.NOT_IN_GROUP
        if command == Command.GET_BATTLES:
            if self.db.is_in_group(username):
                group = self.db.get_group(username)
                group_directory = get_group_directory(group.name)
                battles_directory = group_directory / "battles"
                message = ""
                if battles_directory.exists():
                    for group in battles_directory.glob("*"):
                        group_dir = pathlib.Path(group)
                        message += group_dir.name + ":"
                        for f in group_dir.rglob("*"):
                            message += f"{f.name},"
                        message = message[:-1]
                        message += "|"
                    message = message[:-1]
                    return_code = Codes.OK
            else:
                return_code = Codes.NOT_IN_GROUP
        if command == Command.GET_RESULTS:
            return_code = Codes.OK
            self.__server_socket.send_message_secure(
                f"{verification_code}|{message}|{return_code.value}")
            self.__server_socket.receive_message_secure()
            self.__server_socket.send_file(RESULTS_FILE)
            return username, command
        if command == Command.DOWNLOAD_BATTLE:
            if self.db.is_in_group(username):
                group = self.db.get_group(username)
                enemy, file = details.split("/")
                battles = get_group_directory(group.name) / "battles" / enemy / file
                if battles.exists():
                    return_code = Codes.OK
                    self.__server_socket.send_message_secure(
                        f"{verification_code}|{message}|{return_code.value}")
                    self.__server_socket.receive_message_secure()
                    self.__server_socket.send_file(battles)
                    return username, command
        if command == Command.DOWNLOAD_FILE:
            if self.db.is_in_group(username):
                group = self.db.get_group(username)
                group_directory = get_group_directory(group.name) / DEVELOPMENT_CODE_DIR
                if group_directory.exists():
                    for file_path in group_directory.rglob("*"):
                        if file_path.name == details:
                            return_code = Codes.OK
                            self.__server_socket.send_message_secure(
                                f"{verification_code}|{message}|{return_code.value}")
                            self.__server_socket.receive_message_secure()
                            self.__server_socket.send_file(group_directory / file_path)
                            return username, command
            return_code = Codes.FAILED_TO_FIND_FILE

        self.__server_socket.send_message_secure(f"{verification_code}|{message}|{return_code.value}")
        print(f"{self.__server_socket.receive_message_secure()}")
        return username, command

    def send_message(self, message: str) -> Codes:
        self.__server_socket.send_message_secure(message)
        return self.__server_socket.receive_message_secure(KILO_BYTE)

    def send_file(self, file_path: pathlib.Path, chunk_size: int = KILO_BYTE) -> Codes:
        return self.__server_socket.send_file(file_path, chunk_size)
