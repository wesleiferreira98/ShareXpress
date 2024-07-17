from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QProgressBar
class FileItemWidget(QWidget):
    def __init__(self, file_name):
        super().__init__()
        
        layout = QHBoxLayout()
        
        self.pause_button = QPushButton("⏸", self)
        layout.addWidget(self.pause_button)

        self.file_name_label = QLabel(file_name, self)
        layout.addWidget(self.file_name_label)
        
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)
    
        
        self.setLayout(layout)
