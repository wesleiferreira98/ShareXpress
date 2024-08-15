from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QMessageBox
from app.network.server_discovery import ServerDiscovery

# Classe de diálogo que exibirá a lista de servidores encontrados
class ServerDiscoveryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Servidores Disponíveis")
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
                    border-radius: 6px;
                    width: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #0D47A1;
                    width: 5px;
                }
                QListWidget {
                    background-color: #3e3e3e;
                    border: 1px solid #3e3e3e;
                    border-radius: 5px;
                }
                QLineEdit {
                    background-color: #3e3e3e;
                    border: 1px solid #0D47A1;
                    padding: 7px;
                    border-radius: 5px;
                    color: #f0f0f0;
                }
                QListWidget{
                    background-color: #3e3e3e;
                    border: 1px solid #0D47A1;
                    padding: 7px;
                    border-radius: 5px;
                    color: #f0f0f0; 
                }
                QLabel {
                    
                    padding: 5px;
                    border-radius: 5px;
                    color: #f0f0f0;
                }
            """)
        self.setLayout(QVBoxLayout())
        self.server_list = QListWidget(self)
        self.layout().addWidget(self.server_list)

        self.select_button = QPushButton("Selecionar Servidor", self)
        self.select_button.clicked.connect(self.select_server)
        self.layout().addWidget(self.select_button)

        # Thread de descoberta de servidores
        self.discovery_thread = ServerDiscovery()
        self.discovery_thread.server_found.connect(self.add_server)
        self.discovery_thread.start()

        self.selected_server = None

    def add_server(self, addr):
        server_info = f"{addr[0]}:{addr[1]}"
        self.server_list.addItem(server_info)

    def select_server(self):
        selected_item = self.server_list.currentItem()
        if selected_item:
            self.selected_server = selected_item.text()
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Nenhum servidor selecionado!")

    def closeEvent(self, event):
        self.discovery_thread.stop()
        event.accept()
