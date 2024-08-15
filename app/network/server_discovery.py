import socket
from PyQt5.QtCore import pyqtSignal, QThread
# Classe responsável por descobrir servidores na rede usando QThread
class ServerDiscovery(QThread):
    server_found = pyqtSignal(tuple)  # Sinal que será emitido quando um servidor for encontrado

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(3)  # Timeout de 3 segundos para não travar a interface

        # Enviar uma mensagem de broadcast
        message = "DISCOVER_SERVER".encode('utf-8')
        sock.sendto(message, ('<broadcast>', 12345))  # Porta de broadcast definida

        while self.running:
            try:
                data, addr = sock.recvfrom(1024)  # Buffer de 1024 bytes
                print(data.decode('utf-8'))
                if data.decode('utf-8') == "SERVER_HERE" or data.decode('utf-8') == "SERVER_HERE:12345":
                    self.server_found.emit(addr)
            except socket.timeout:
                break

        sock.close()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()