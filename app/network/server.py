import os
import socket
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import json
import time
import pyperclip  # Biblioteca para acessar a área de transferência

class ClientHandler(QThread):
    progress_updated = pyqtSignal(int, str)
    message = pyqtSignal(str)

    def __init__(self, client_socket, save_dir):
        super().__init__()
        self.client_socket = client_socket
        self.save_dir = save_dir

    def run(self):
        with self.client_socket:
            file_info = self.client_socket.recv(2048).decode('utf-8')
            if file_info:
                try:
                    # Tentando decodificar como UTF-8
                    file_name, file_size = file_info.split(',')
                    file_size = int(file_size)
                except Exception:
                    # Tentando decodificar como JSON
                    file_info = json.loads(file_info)
                    file_name = file_info['fileName']
                    file_size = int(file_info['fileSize'])
                    content = file_info['content']
                
                self.client_socket.sendall(b"OK\n")
                
                if file_name == "clipboard_content":
                    pyperclip.copy(content)
                    self.message.emit("Conteúdo da área de transferência recebido e copiado com sucesso")
                else:
                    file_path = os.path.join(self.save_dir, file_name)
                    
                    start_time = time.time()
                    chunk_size = 10 * 1024 * 1024  # Ajustar para receber blocos de 10MB
                    with open(file_path, 'wb') as f:
                        bytes_received = 0
                        while bytes_received < file_size:
                            chunk = self.client_socket.recv(chunk_size)
                            if not chunk:
                                break
                            f.write(chunk)
                            bytes_received += len(chunk)
                            progress = int((bytes_received / file_size) * 100)
                            elapsed_time = time.time() - start_time
                            estimated_total_time = (elapsed_time / bytes_received) * file_size
                            remaining_time = estimated_total_time - elapsed_time
                            estimated_time = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
                            self.progress_updated.emit(progress, estimated_time)

                    self.client_socket.sendall(b"OK\n")
                    self.message.emit(f"Arquivo {file_name} recebido com sucesso")

class FileServer(QThread):
    progress_updated = pyqtSignal(int, str)
    message = pyqtSignal(str)

    def __init__(self, host='0.0.0.0', port=12345):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
        self.save_dir = os.path.join(os.path.expanduser("~"), "ShareXpress")
        self.client_threads = []

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(100)
        self.running = True
        self.message.emit("Servidor iniciado, aguardando conexão...")

        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                self.message.emit(f"Conexão de {addr}")

                # Finaliza threads anteriores se ainda estiverem ativas
                self.cleanup_threads()

                client_handler = ClientHandler(client_socket, self.save_dir)
                client_handler.progress_updated.connect(self.handle_progress_update)
                client_handler.message.connect(self.handle_message)
                client_handler.start()
                self.client_threads.append(client_handler)
            except OSError:
                break

    def cleanup_threads(self):
        for thread in self.client_threads:
            if thread.isRunning():
                thread.quit()
                thread.wait()
        self.client_threads = []

    def handle_progress_update(self, progress, estimated_time):
        self.progress_updated.emit(progress, estimated_time)

    def handle_message(self, message):
        self.message.emit(message)

    def stop_server(self):
        self.running = False
        self.server_socket.close()
        self.message.emit("Servidor parado")
        self.cleanup_threads()
