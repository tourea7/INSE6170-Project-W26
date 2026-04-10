from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.scanner import scan_networks

class ScanWorker(QThread):
    finished = pyqtSignal(list)
    
    def run(self):
        devices = scan_networks()
        self.finished.emit(devices)

class DevicesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("Connected IoT Devices")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        self.scan_button = QPushButton(" Scan Network")    
        self.scan_button.clicked.connect(self.scan_devices)
        layout.addWidget(self.scan_button)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["IP Address", "MAC Address", "Vendor", "Last Seen"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
    def scan_devices(self):
        self.scan_button.setText("Scanning...")
        self.scan_button.setEnabled(False)
        
        self.thread = QThread()
        self.worker = ScanWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_scan_done)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()
        
    def on_scan_done(self, devices):
        self.table.setRowCount(len(devices))
        for row, device in enumerate(devices):
            self.table.setItem(row, 0, QTableWidgetItem(device["ip"]))
            self.table.setItem(row, 1, QTableWidgetItem(device["mac"]))
            self.table.setItem(row, 2, QTableWidgetItem(device["vendor"]))
            self.table.setItem(row, 3, QTableWidgetItem(device["last_seen"]))
        self.scan_button.setText("Scan Network")
        self.scan_button.setEnabled(True)
            
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = DevicesTab()
    window.show()
    sys.exit(app.exec_())