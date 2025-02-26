import tkinter as tk
from GUI.networking import ClientSocket

class LoginPage(tk.Frame):
    def __init__(self, client_socket: ClientSocket, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.client_socket = client_socket
        self.username_label = tk.Label(self, text="Userid:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()

        self. password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.validate_login)
        self.login_button.pack()


    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.client_socket.username = username
        self.client_socket.password = password
        if self.client_socket.validate_user():
            self.l = tk.Label(self, text="Correct!")
            self.l.pack()
        else:
            self.l = tk.Label(self, text="Incorrect username or password!")
            self.l.pack()