import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.database import init_db

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Launch application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())