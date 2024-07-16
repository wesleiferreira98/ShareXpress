import socket

class FileServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server started, waiting for connection...")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            # Aqui você pode adicionar a lógica para receber e salvar arquivos

    def stop_server(self):
        self.server_socket.close()
