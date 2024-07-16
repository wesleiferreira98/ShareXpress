from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from .send_screen import SendScreen
from .receive_screen import ReceiveScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Transfer App")
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
