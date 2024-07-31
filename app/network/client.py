import socket
import os
from PyQt5.QtCore import QThread, pyqtSignal
import time

class FileClient(QThread):
    progress_updated = pyqtSignal(int, str)
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
            chunk_size = 10 * 1024 * 1024  # Dividir em blocos de 10MB

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(30)  # Definir timeout de 10 segundos
                s.connect((self.ip, self.port))
                
                # Enviar informações do arquivo (nome e tamanho)
                file_info = f"{file_name},{file_size}\n".encode()  # Adiciona \n para demarcar o fim da mensagem
                s.sendall(file_info)

                # Espera uma confirmação de recebimento do servidor
                confirmation = s.recv(1024)
                if confirmation != b"OK\n" and confirmation != b"OK":
                    raise RuntimeError("Falha na confirmação do servidor")

                # Pequena pausa antes de enviar o arquivo
                time.sleep(0.1)
                start_time = time.time()
                # Enviar o arquivo em blocos
                with open(self.file_path, 'rb') as f:
                    bytes_sent = 0
                    while True:
                        bytes_read = f.read(chunk_size)
                        if not bytes_read:
                            break
                        s.sendall(bytes_read)
                        bytes_sent += len(bytes_read)
                        progress = int((bytes_sent / file_size) * 100)
                        print(f"Enviado: {bytes_sent} de {file_size} bytes")

                        # Calcular tempo estimado
                        elapsed_time = time.time() - start_time
                        estimated_total_time = (elapsed_time / bytes_sent) * file_size
                        estimated_time_remaining = estimated_total_time - elapsed_time
                        estimated_time_str = time.strftime("%M:%S", time.gmtime(estimated_time_remaining))
                        
                        self.progress_updated.emit(progress, estimated_time_str)

                # Espera confirmação de recebimento do servidor
                final_confirmation = s.recv(1024)
                if final_confirmation == b"OK" or final_confirmation == b"OK\n":
                    print(f"Arquivo {self.file_path} enviado com sucesso.")
                else:
                    raise RuntimeError("Falha na confirmação final do servidor")
        except Exception as e:
            print(f"Failed to send file {self.file_path}. Error: {e}")

    def stop_client(self):
        self.terminate()  # Termina a thread do cliente se necessário
