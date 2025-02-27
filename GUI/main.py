import socket
import tkinter as tk
from networking import ClientSocket, SocketWrapper
from GUI.pages import BattlePage
from GUI.pages import GroupManagementPage
from GUI.pages import CodePage
from GUI.pages import LoginPage
from GUI.pages import TournamentPage
from GUI.pages import SignUpPage

class MainView(tk.Frame):
    def __init__(self, client_socket: ClientSocket, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.client_socket = client_socket
        self.login_page = LoginPage(self.client_socket,self)
        self.code_page = CodePage(self.client_socket,self)
        self.group_page = GroupManagementPage(self.client_socket, self)
        self.tournament_page = TournamentPage(self.client_socket,self)
        self.battle_page = BattlePage(self.client_socket,self)
        self.sign_up_page = SignUpPage(self.client_socket, self)

        button_frame = tk.Frame(self)
        self.container = tk.Frame(self)
        button_frame.pack(side="top", fill="x", expand=False)
        self.container.pack(side="top", fill="both", expand=True)

        self.login_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.code_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.group_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.tournament_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.battle_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.sign_up_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)


        login_page_button = tk.Button(button_frame, text="Login", command=self.create_login_page)
        code_page_button = tk.Button(button_frame, text="Code", command=self.create_code_page)
        group_page_button = tk.Button(button_frame, text="Group", command=self.create_group_page)
        tournament_page_button = tk.Button(button_frame, text="Tournament", command=self.create_tournament_page)
        battle_page_button = tk.Button(button_frame, text="Battle", command=self.create_battle_page)
        sign_up_page_button = tk.Button(button_frame, text="sign up", command=self.create_sign_up_page)


        login_page_button.pack(side="left")
        code_page_button.pack(side="left")
        group_page_button.pack(side="left")
        tournament_page_button.pack(side="left")
        battle_page_button.pack(side="left")
        sign_up_page_button.pack(side="left")

        self.login_page.lift()

    def create_sign_up_page(self):
        self.sign_up_page.destroy()
        self.sign_up_page = SignUpPage(self.client_socket, self)
        self.sign_up_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.sign_up_page.lift()

    def create_group_page(self):
        self.group_page.destroy()
        self.group_page = GroupManagementPage(self.client_socket, self)
        self.group_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.group_page.lift()

    def create_login_page(self):
        self.login_page.destroy()
        self.login_page = LoginPage(self.client_socket, self)
        self.login_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.login_page.lift()

    def create_code_page(self):
        self.code_page.destroy()
        self.code_page = CodePage(self.client_socket,self)
        self.code_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.code_page.lift()

    def create_tournament_page(self):
        self.tournament_page.destroy()
        self.tournament_page = TournamentPage(self.client_socket, self)
        self.tournament_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.tournament_page.lift()

    def create_battle_page(self):
        self.battle_page.destroy()
        self.battle_page = BattlePage(self.client_socket, self)
        self.battle_page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.battle_page.lift()


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connecting with Server
    sock.connect((host, port))
    s = ClientSocket(SocketWrapper(sock))
    root = tk.Tk()
    main = MainView(s, root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()
