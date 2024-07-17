import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox, QApplication
from PyQt5.QtCore import Qt, pyqtSlot
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
        self.file_server = FileServer()  # Inicializa FileServer como um QThread

        # Conectar sinais de FileServer aos slots da ReceiveScreen
        self.file_server.message.connect(self.show_message)
        self.file_server.progress_updated.connect(self.update_progress)

    def get_ip_address(self):
        import socket
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
            self.server_running = False
            self.server_button.setText("Iniciar Servidor")

    def closeEvent(self, event):
        if self.server_running:
            self.file_server.stop_server()
            self.file_server.wait()
        event.accept()

