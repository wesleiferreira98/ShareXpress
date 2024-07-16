import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog, QLineEdit, QLabel, QListWidget, QProgressBar, QDialog
from PyQt5.QtCore import Qt
import threading
import socket

from app.network.server import FileServer

class ReceiveScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Receber Arquivos")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        self.ip_label = QLabel(f"Endereço IP: {self.get_ip_address()}")
        layout.addWidget(self.ip_label)

        self.port_label = QLabel("Porta: 12345")
        layout.addWidget(self.port_label)

        self.server_button = QPushButton("Iniciar Servidor", self)
        self.server_button.clicked.connect(self.toggle_server)
        layout.addWidget(self.server_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.server_running = False
        self.server_thread = None
        self.file_server = FileServer()  # Certifique-se de inicializar o servidor aqui

    def get_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def toggle_server(self):
        if self.server_running:
            self.file_server.stop_server()
            if self.server_thread is not None:
                self.server_thread.join()
            self.server_running = False
            self.server_button.setText("Iniciar Servidor")
            QMessageBox.information(self, "Servidor", "Servidor parado com sucesso!")
        else:
            self.server_thread = threading.Thread(target=self.file_server.start_server)
            self.server_thread.start()
            self.server_running = True
            self.server_button.setText("Encerrar Servidor")
            QMessageBox.information(self, "Servidor", "Servidor iniciado com sucesso!")