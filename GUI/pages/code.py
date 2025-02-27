import pathlib
import tkinter as tk
from tkinter import filedialog
from GUI.networking import ClientSocket
from GUI.networking import Codes, Command

class CodePage(tk.Frame):
    def __init__(self, client_socket: ClientSocket, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.client_socket = client_socket
        open_button = tk.Button(self, text="Open File", command=self.open_file_dialog)
        open_button.pack(padx=20, pady=20)

        self.selected_file_label = tk.Label(self, text="Selected File:")
        self.selected_file_label.pack()

        self.file_text = tk.Text(self, wrap=tk.WORD, height=10, width=40)
        self.file_text.pack(padx=20, pady=20)
        self.show_files()

    def show_files(self):
        _, m = self.client_socket.send_command(Command.IS_IN_GROUP)
        if m != Codes.HAS_GROUP:
            return
        _, m = self.client_socket.send_command(Command.GET_FILES)
        files = m.split(",")
        for file_name in files:
            frame = tk.Frame(self)
            frame.pack(fill="x", padx=5, pady=2)

            label = tk.Label(frame, text=file_name, anchor="w")
            label.pack(side="left", expand=True, fill="x")

            button = tk.Button(frame, text="Download", command=lambda f=file_name: self.download_file(f))
            button.pack(side="right")

    def download_file(self, file_name):
        return_code, _ = self.client_socket.send_command(Command.DOWNLOAD_FILE, details=file_name)
        if return_code == Codes.OK:
            self.client_socket.receive_file(pathlib.Path(f"development/{file_name}"))

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Select a File",
                                               filetypes=[("python file", "*.py"), ("All files", "*.*")])
        if file_path:
            self.selected_file_label.config(text=f"Selected File: {file_path}")
            self.process_file(file_path)

    def process_file(self, file_path):
        return_code, _ = self.client_socket.send_command(Command.UPLOAD_FILE)
        self.client_socket.send_file(pathlib.Path(file_path))

