import os
import socket
import sys
from PyQt5.QtWidgets import QApplication, QListWidgetItem,QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QFileDialog, QLineEdit, QLabel, QListWidget, QProgressBar, QDialog, QProgressDialog, QFrame
from PyQt5.QtCore import Qt, pyqtSlot, QPropertyAnimation
from app.gui.components.file_item_widget import FileItemWidget
from app.network.client import FileClient
class SendScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enviar Arquivos")
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #5e5e5e;
                border: 1px solid #5e5e5e;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #7e7e7e;
            }
            QPushButton:pressed {
                background-color: #3e3e3e;
            }
            QProgressBar {
                background-color: #3e3e3e;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #5e5e5e;
                width: 20px;
            }
            QListWidget {
                background-color: #3e3e3e;
                border: 1px solid #3e3e3e;
                border-radius: 5px;
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
            }
        """)
        self.setGeometry(300, 300, 800, 600)

        main_layout = QHBoxLayout()
        
        self.menu_frame = QFrame(self)
        self.menu_frame.setFixedWidth(250)
        menu_layout = QVBoxLayout()
        
        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("Endereço IP")
        menu_layout.addWidget(self.ip_input)

        self.port_input = QLineEdit(self)
        self.port_input.setPlaceholderText("Porta")
        menu_layout.addWidget(self.port_input)

        self.test_connection_button = QPushButton("Testar Conexão", self)
        self.test_connection_button.clicked.connect(self.test_connection)
        menu_layout.addWidget(self.test_connection_button)
        
        self.menu_frame.setLayout(menu_layout)
        self.menu_frame.setVisible(False)
        
        self.toggle_menu_button = QPushButton("☰", self)
        self.toggle_menu_button.clicked.connect(self.toggle_menu)
        self.toggle_menu_button.setFixedSize(40, 40)
        
        content_layout = QVBoxLayout()
        content_layout.addWidget(self.toggle_menu_button)
        
        self.file_list = QListWidget(self)
        content_layout.addWidget(self.file_list)

        self.select_files_button = QPushButton("Selecionar Arquivos", self)
        self.select_files_button.clicked.connect(self.open_file_dialog)

        self.send_files_button = QPushButton("Enviar Arquivos", self)
        self.send_files_button.clicked.connect(self.send_files)

        # Layout para os botões
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.select_files_button)
        buttons_layout.addWidget(self.send_files_button)
        
        content_layout.addLayout(buttons_layout)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        
        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(content_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    
    def open_file_dialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Selecionar Arquivos", "", "All Files (*)", options=options)
        self.files = []
        if files:
            for file in files:
                file_name = os.path.basename(file)
                self.files.append(file)
                item = QListWidgetItem(self.file_list)
                item_widget = FileItemWidget(file_name)
                item.setSizeHint(item_widget.sizeHint())
                self.file_list.addItem(item)
                self.file_list.setItemWidget(item, item_widget)

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
        progress_dialog = QProgressDialog("Enviando arquivos...", "Cancelar", 0, len(self.files), self)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.show()

        self.client_threads = []

        for file in self.files:
            client_thread = FileClient(ip, port, file)
            client_thread.progress_updated.connect(progress_dialog.setValue)
            client_thread.message.connect(self.show_message)
            self.client_threads.append(client_thread)

        for client_thread in self.client_threads:
            client_thread.start()

            

    @pyqtSlot(str)
    def show_message(self, message):
        QMessageBox.information(self, "Envio de Arquivos", message)

    
    def toggle_menu(self):
        if self.menu_frame.isVisible():
            self.animate_menu(True)
            self.menu_frame.setVisible(False)
        else:
            self.menu_frame.setVisible(True)
            self.animate_menu(True)

    def animate_menu(self, show):
        width = 250 if show else 0
        animation = QPropertyAnimation(self.menu_frame, b"minimumWidth")
        animation.setDuration(300)
        animation.setStartValue(self.menu_frame.width())
        animation.setEndValue(width)
        animation.finished.connect(lambda: self.menu_frame.setVisible(show))
        animation.start()