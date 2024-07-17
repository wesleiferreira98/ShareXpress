from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from .send_screen import SendScreen
from .receive_screen import ReceiveScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ShareXpress")
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
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #5e5e5e;
                width: 20px;
            }
            QListWidget {
                background-color: #3e3e3e;
                border: 1px solid #3e3e3e;
            }
            QLineEdit {
                background-color: #3e3e3e;
                border: 1px solid #5e5e5e;
                padding: 5px;
                border-radius: 5px;
                color: #f0f0f0;
            }
            QLabel {
                color: #f0f0f0;
            }
        """)
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        self.send_button = QPushButton("Enviar Arquivos", self)
        self.send_button.clicked.connect(self.show_send_screen)
        layout.addWidget(self.send_button)

        self.receive_button = QPushButton("Receber Arquivos", self)
        self.receive_button.clicked.connect(self.show_receive_screen)
        layout.addWidget(self.receive_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_send_screen(self):
        self.send_screen = SendScreen()
        self.send_screen.show()

    def show_receive_screen(self):
        self.receive_screen = ReceiveScreen()
        self.receive_screen.show()
