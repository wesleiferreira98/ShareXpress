import socket
import os
from PyQt5.QtCore import QThread, pyqtSignal
import time

class FileClient(QThread):
    progress_updated = pyqtSignal(int)
    message = pyqtSignal(str)

    def __init__(self, ip, port, file_path):
        super().__init__()
        self.ip = ip
        self.port = port
        self.file_path = file_path

    def run(self):
        try:
            file_name = os.path.basename(self.file_path)
            file_size = os.path.getsize(self.file_path)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)  # Definir timeout de 10 segundos
                s.connect((self.ip, self.port))
                
                # Enviar informações do arquivo (nome e tamanho)
                file_info = f"{file_name},{file_size}\n".encode()  # Adiciona \n para demarcar o fim da mensagem
                s.sendall(file_info)

                # Espera uma confirmação de recebimento do servidor
                confirmation = s.recv(1024)
                if confirmation != b"OK":
                    raise RuntimeError("Falha na confirmação do servidor")

                # Pequena pausa antes de enviar o arquivo
                time.sleep(0.1)

                # Enviar o arquivo
                with open(self.file_path, 'rb') as f:
                    bytes_sent = 0
                    while True:
                        bytes_read = f.read(4096)
                        if not bytes_read:
                            break
                        s.sendall(bytes_read)
                        bytes_sent += len(bytes_read)
                        progress = int((bytes_sent / file_size) * 100)
                        self.progress_updated.emit(progress)
                        print(f"Enviado: {bytes_sent} de {file_size} bytes")

                # Espera confirmação de recebimento do servidor
                final_confirmation = s.recv(1024)
                if final_confirmation == b"OK":
                    print(f"Arquivo {self.file_path} enviado com sucesso.")
                else:
                    raise RuntimeError("Falha na confirmação final do servidor")
        except Exception as e:
            print(f"Failed to send file {self.file_path}. Error: {e}")

    def stop_client(self):
        self.terminate()  # Termina a thread do cliente se necessário

