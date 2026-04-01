from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget
from PyQt5.QtCore import Qt
import sys
from tab_devices import DevicesTab
from tab_capture import CaptureTab
from tab_firewall import FirewallTab
from tab_ips import IPSTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart IoT Router")
        self.setMinimumSize(900, 600)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create empty tabs
        self.tab_devices = DevicesTab()
        self.tab_capture = CaptureTab()
        self.tab_firewall = FirewallTab()
        self.tab_ips = IPSTab()
        self.tab_logs = QWidget()
        
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