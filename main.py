import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from app.gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Definindo o caminho absoluto para o ícone
    script_dir = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(script_dir, 'app', 'gui', 'assets', 'app_icon.png')
    
    # Configurando o ícone do aplicativo
    app.setWindowIcon(QIcon(icon_path))
    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
