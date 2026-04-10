from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget
from PyQt5.QtCore import Qt
import sys
from tab_devices import DevicesTab
from tab_capture import CaptureTab
from tab_firewall import FirewallTab
from tab_ips import IPSTab
from tab_logs import LogsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart IoT Router")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #2c3e50;
                color: white;
                padding: 8px 20px;
                margin-right: 2px;
                border-radius: 4px 4px 0 0;
                font-size: 13px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background-color: #2980b9;
                color: white;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                border: none;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
            QTableWidget {
                gridline-color: #e0e0e0;
                font-size: 12px;
                border: 1px solid #cccccc;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 8px;
                font-size: 12px;
                border: none;
            }
            QLabel {
                font-size: 13px;
                color: #2c3e50;
            }
            QLineEdit, QSpinBox {
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QSpinBox:focus {
                border: 1px solid #2980b9;
            }
        """)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create empty tabs
        self.tab_devices = DevicesTab()
        self.tab_capture = CaptureTab()
        self.tab_firewall = FirewallTab()
        self.tab_ips = IPSTab()
        self.tab_logs = LogsTab()
        
        # Add tabs
        self.tabs.addTab(self.tab_devices, "Devices")
        self.tabs.addTab(self.tab_capture, "Packet Capture")
        self.tabs.addTab(self.tab_firewall, "Firewall")
        self.tabs.addTab(self.tab_ips, "IPS")
        self.tabs.addTab(self.tab_logs, "Logs")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())