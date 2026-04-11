import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.database import init_db, delete_old_records

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Delete old records automatically (older than 30 days)
    delete_old_records(days=30)
    
    # Launch application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())