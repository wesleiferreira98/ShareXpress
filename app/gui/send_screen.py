import socket
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog, QLineEdit, QLabel, QListWidget, QProgressBar, QDialog,QProgressDialog
from PyQt5.QtCore import Qt,pyqtSlot
from app.network.client import FileClient
class SendScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enviar Arquivos")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        self.file_list = QListWidget(self)
        layout.addWidget(self.file_list)

        self.select_files_button = QPushButton("Selecionar Arquivos", self)
        self.select_files_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.select_files_button)

        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("Endereço IP")
        layout.addWidget(self.ip_input)

        self.port_input = QLineEdit(self)
        self.port_input.setPlaceholderText("Porta")
        layout.addWidget(self.port_input)

        self.test_connection_button = QPushButton("Testar Conexão", self)
        self.test_connection_button.clicked.connect(self.test_connection)
        layout.addWidget(self.test_connection_button)

        self.send_files_button = QPushButton("Enviar Arquivos", self)
        self.send_files_button.clicked.connect(self.send_files)
        layout.addWidget(self.send_files_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Selecionar Arquivos", "", "All Files (*)", options=options)
        if files:
            self.file_list.addItems(files)

    def test_connection(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        try:
            with socket.create_connection((ip, port), timeout=10):
                QMessageBox.information(self, "Conexão", "Conexão bem-sucedida!")
        except Exception as e:
            QMessageBox.critical(self, "Conexão", f"Falha na conexão: {e}")

    def send_files(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]

        progress_dialog = QProgressDialog("Enviando arquivos...", "Cancelar", 0, len(files), self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.show()

        self.client_threads = []

        for file in files:
            client_thread = FileClient(ip, port, file)
            client_thread.progress_updated.connect(progress_dialog.setValue)
            client_thread.message.connect(self.show_message)
            self.client_threads.append(client_thread)

        for client_thread in self.client_threads:
            client_thread.start()

            

    @pyqtSlot(str)
    def show_message(self, message):
        QMessageBox.information(self, "Envio de Arquivos", message)
