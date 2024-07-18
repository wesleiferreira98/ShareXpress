import os
import socket
from PyQt5.QtCore import QThread, pyqtSignal

class FileServer(QThread):
    progress_updated = pyqtSignal(int)
    message = pyqtSignal(str)

    def __init__(self, host='0.0.0.0', port=12345):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Adiciona essa linha para permitir reutilização do endereço
        self.running = False
        self.save_dir = os.path.join(os.path.expanduser("~"), "ShareXpress")

        # Cria o diretório ShareXpress se não existir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        self.message.emit("Server started, waiting for connection...")

        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                self.message.emit(f"Connection from {addr}")
                self.handle_client(client_socket)
            except OSError:
                break

    def handle_client(self, client_socket):
        with client_socket:
            file_info = client_socket.recv(1024).decode()
            if file_info:
                client_socket.sendall(b"OK")  # Confirmação de recebimento do cabeçalho
                file_name, file_size = file_info.split(',')
                file_path = os.path.join(self.save_dir, file_name)
                file_size = int(file_size)

                with open(file_path, 'wb') as f:
                    bytes_received = 0
                    while bytes_received < file_size:
                        chunk = client_socket.recv(1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        bytes_received += len(chunk)
                        progress = int((bytes_received / file_size) * 100)
                        self.progress_updated.emit(progress)

                # Enviar confirmação de recebimento ao cliente
                client_socket.sendall(b"OK")

    def stop_server(self):
        self.running = False
        self.server_socket.close()
        self.message.emit("Server stopped")
