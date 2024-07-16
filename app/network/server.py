import os
import socket

class FileServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        self.save_dir = os.path.join(os.path.expanduser("~"), "ShareXpress")

        # Cria o diretório ShareXpress se não existir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print("Server started, waiting for connection...")

        while self.running:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        with client_socket:
            file_info = client_socket.recv(1024).decode()
            if file_info:
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

                print(f"File {file_name} received and saved to {file_path}")

    def stop_server(self):
        self.running = False
        self.server_socket.close()
        print("Server stopped")
