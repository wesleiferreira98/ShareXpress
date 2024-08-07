from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QProgressBar, QVBoxLayout

class FileItemWidget(QWidget):
    def __init__(self, file_name):
        super().__init__()
        main_layout = QVBoxLayout()
        
        layout = QHBoxLayout()

        layoutQlabel = QVBoxLayout()

        
        self.pause_button = QPushButton("⏸", self)
        self.pause_button.setFixedSize(40, 40)  # Define um tamanho fixo para o botão
        layout.addWidget(self.pause_button)
        
        self.file_name_label = QLabel(file_name, self)
        layout.addWidget(self.file_name_label)
        self.percentage_label = QLabel("0%", self)
        layoutQlabel.addWidget(self.percentage_label)
        self.estimated_time_label = QLabel("Tempo estimado: --:--", self)
        layoutQlabel.addWidget(self.estimated_time_label)
        layout.addLayout(layoutQlabel)
        
        main_layout.addLayout(layout)

        
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFormat("") 
        self.progress_bar.setFixedHeight(10)
        # Adiciona bordas arredondadas à barra de progresso
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3e3e3e;
                border-radius: 10px;
                background-color: #3e3e3e;
                text-align: center;
            }
            QProgressBar::chunk {
                border-radius: 10px;
                background-color: #0D47A1;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        # Labels para mostrar a porcentagem e o tempo estimado
       
        
        self.setLayout(main_layout)

    def update_progress(self, progress, estimated_time):
        self.progress_bar.setValue(progress)
        self.percentage_label.setText(f"{progress}%")
        self.estimated_time_label.setText(f"Tempo estimado: {estimated_time}")
