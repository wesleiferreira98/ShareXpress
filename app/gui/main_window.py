from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from .send_screen import SendScreen
from .receive_screen import ReceiveScreen
import os

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
                border-radius: 14px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #7e7e7e;
            }
            QPushButton:pressed {
                background-color: #3e3e3e;
            }
            QLabel {
                color: #f0f0f0;
            }
        """)
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addSpacerItem(QSpacerItem(30, 30))

        title_label = QLabel("Escolha o modo de funcionamento")
        title_label.setAlignment(Qt.AlignCenter)

         # Aumentar o tamanho da fonte do título
        title_font = QFont()
        title_font.setPointSize(20)  # Defina o tamanho da fonte desejado
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Adicionar espaço menor entre o título e os botões
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        layout.addSpacerItem(QSpacerItem(100, 100))

        icon_path =  os.path.join(scriptDir, 'assets')

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(50)  # Adicionar espaço entre os botões

        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'upload-na-nuvem.png'))))
        self.send_button.setIconSize(QSize(100, 100))
        self.send_button.setFixedSize(150, 150)
        self.send_button.setToolTip("Enviar Arquivos") 
        self.send_button.clicked.connect(self.show_send_screen)
        button_layout.addWidget(self.send_button)

        self.receive_button = QPushButton()
        self.receive_button.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'download-da-nuvem.png'))))
        self.receive_button.setIconSize(QSize(100, 100))
        self.receive_button.setFixedSize(150, 150)
        self.receive_button.setToolTip("Receber Arquivos") 
        self.receive_button.clicked.connect(self.show_receive_screen)
        button_layout.addWidget(self.receive_button)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_send_screen(self):
        self.send_screen = SendScreen()
        self.send_screen.show()

    def show_receive_screen(self):
        self.receive_screen = ReceiveScreen()
        self.receive_screen.show()
