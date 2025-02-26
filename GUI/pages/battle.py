import pathlib
import re
import tkinter as tk
from tkinter import messagebox

from GUI.db.group import Group
from GUI.networking import ClientSocket, Codes, Command

class BattlePage(tk.Frame):
    def __init__(self, client_socket: ClientSocket, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.client_socket = client_socket
        username_label = tk.Label(self, text="Battle")
        username_label.pack()
        self.file_buttons = []
        self.name_frame = tk.Frame(self)
        self.name_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.file_frame = tk.Frame(self)
        self.file_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        self.l = None
        # self.show_available_groups()
        self.show_battles()

    def show_battles(self):
        _, m = self.client_socket.send_command(Command.IS_IN_GROUP)
        if m != Codes.HAS_GROUP:
            return
        _, m = self.client_socket.send_command(Command.GET_BATTLES)
        group_files = m.split("|")
        battles = []
        for group_file in group_files:
            group, f = group_file.split(":")
            battles.append([group, f.split(",")])
        print(f"{battles=}")
        for name, files in battles:
            btn = tk.Button(self.name_frame, text=name, command=lambda n=name, f=files: self.show_files(n, f))
            btn.pack(fill=tk.X, pady=2)

    def show_files(self, group_name, files):
        for btn in self.file_buttons:
            btn.destroy()
        self.file_buttons.clear()
        print(group_name)
        for file in files:
            btn = tk.Button(self.file_frame, text=file, command=lambda f=file: self.download_battle(group_name, f))
            btn.pack(fill=tk.X, pady=2)
            self.file_buttons.append(btn)

    def show_available_groups(self) -> None:
        return_code, groups_message = self.client_socket.send_command(command=Command.GET_GROUPS)
        print(return_code)
        print(f"{return_code=}, {groups_message=}")
        _, user_group = self.client_socket.send_command(command=Command.GET_USER_GROUP)
        if return_code != Codes.OK:
            return

        pattern = r"\((\w+),\[(.*?)\],(\w+)\)"

        matches = re.findall(pattern, groups_message)
        print(matches)
        self.groups = []
        for match in matches:
            group_name, users, owner = match
            users = users.replace("'", "")
            users = users.replace(" ", "")
            if group_name != user_group:
                self.groups.append(Group(group_name, users.split(","), owner))

        self.listbox = tk.Listbox(self, font=("Arial", 14))
        for group in self.groups:
            self.listbox.insert(tk.END, group.name)
        self.listbox.pack(pady=10)

        self.users_label = tk.Label(self, text="Select a group", font=("Arial", 12), justify="left")
        self.users_label.pack(pady=5)

        self.listbox.bind("<<ListboxSelect>>", self.show_users)

    def show_users(self, event):
        if self.l is not None:
            self.l.destroy()
        selected_group_name = self.listbox.get(self.listbox.curselection())
        self.selected_group = next(group for group in self.groups if group.name == selected_group_name)
        text = f"Users in {self.selected_group.name}:\nOwner: {self.selected_group.owner}\n"
        for user in self.selected_group.users:
            if user != self.selected_group.owner:
                text += f"{user}\n"
        self.users_label.config(text=text)

    def download_battle(self,group_name, file_name):
        return_code, _ = self.client_socket.send_command(Command.DOWNLOAD_BATTLE, details=f"{group_name}/{file_name}")
        if return_code == Codes.OK:
            self.client_socket.receive_file(pathlib.Path(f"battles/{group_name}/{file_name}"))

