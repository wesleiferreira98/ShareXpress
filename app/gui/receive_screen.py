import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QApplication
from PyQt5.QtCore import Qt, pyqtSlot
from app.network.server import FileServer
import socket

class ReceiveScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Receber Arquivos")
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #0D47A1;
                border: 1px solid #0D47A1;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0D47A1;
            }
            QPushButton:pressed {
                background-color: #536DFE;
            }
            QProgressBar {
                background-color: #3e3e3e;
                border: 1px solid #3e3e3e;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #5e5e5e;
                width: 10px;
            }
            QListWidget {
                background-color: #3e3e3e;
                border: 1px solid #3e3e3e;
                border-radius: 20px;
            }
            QLineEdit {
                background-color: #3e3e3e;
                border: 1px solid #5e5e5e;
                padding: 5px;
                border-radius: 5px;
                color: #f0f0f0;
            }
             QLabel {
                padding: 5px;
                border-radius: 5px;
                color: #f0f0f0;
                font-size: 18px;  /* Aumenta o tamanho da fonte dos rótulos */
            }
        """)
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Centraliza os widgets no layout
        layout.setSpacing(20)  # Espaçamento entre os widgets

        self.title_label = QLabel("Informações do Servidor")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px;")  # Aumenta o tamanho da fonte do título
        layout.addWidget(self.title_label)

        container = QWidget()
        container.setStyleSheet("background-color: #3e3e3e; border-radius: 15px; padding: 20px;")  # Bordas arredondadas e padding
        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)
        container.setLayout(container_layout)

        self.ip_label = QLabel(f"Endereço IP: {self.get_ip_address()}")
        self.ip_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.ip_label)

        self.port_label = QLabel("Porta: 12345")
        self.port_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.port_label)

        layout.addWidget(container)

        self.server_button = QPushButton("Iniciar Servidor", self)
        self.server_button.clicked.connect(self.toggle_server)
        layout.addWidget(self.server_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.server_running = False
        self.file_server = FileServer()  # Inicializa FileServer como um QThread

        # Conectar sinais de FileServer aos slots da ReceiveScreen
        self.file_server.message.connect(self.show_message)
        self.file_server.progress_updated.connect(self.update_progress)

    def get_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    @pyqtSlot(str)
    def show_message(self, message):
        QMessageBox.information(self, "Servidor de Arquivos", message)

    @pyqtSlot(int)
    def update_progress(self, progress):
        # Implemente a atualização da barra de progresso aqui
        pass

    def toggle_server(self):
        if not self.server_running:
            self.file_server.start()
            self.server_running = True
            self.server_button.setText("Encerrar Servidor")
        else:
            self.file_server.stop_server()
            self.file_server.terminate() # Aguarda a thread terminar
            self.file_server = FileServer()  # Recria a instância do servidor
            self.server_running = False
            self.server_button.setText("Iniciar Servidor")

    def closeEvent(self, event):
        if self.server_running:
            self.file_server.stop_server()
            self.file_server.terminate()
        event.accept()

