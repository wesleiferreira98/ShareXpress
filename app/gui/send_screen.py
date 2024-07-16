import socket
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog, QLineEdit, QLabel, QListWidget, QProgressBar, QDialog,QProgressDialog
from PyQt5.QtCore import Qt
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
            with socket.create_connection((ip, port), timeout=5):
                QMessageBox.information(self, "Conexão", "Conexão bem-sucedida!")
        except Exception as e:
            QMessageBox.critical(self, "Conexão", f"Falha na conexão: {e}")

    def send_files(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        
        progress_dialog = QProgressDialog("Enviando arquivos...", "Cancelar", 0, len(files), self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.show()

        for i, file in enumerate(files):
            progress_dialog.setValue(i)
            if progress_dialog.wasCanceled():
                break
            # Aqui você adiciona a lógica para enviar cada arquivo
            # Por exemplo, use a função send_file que definimos antes
            # self.send_file(file, ip, port)

        progress_dialog.setValue(len(files))
        QMessageBox.information(self, "Envio", "Arquivos enviados com sucesso!")
