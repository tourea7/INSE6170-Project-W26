from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
import sys
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db')
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.scanner import scan_networks

class EditDeviceDialog(QDialog):
    def __init__(self, device_mac, parent=None):
        super().__init__(parent)
        self.device_mac = device_mac
        self.setWindowTitle("Edit Device")
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.vendor_input = QLineEdit()
        self.model_input = QLineEdit()
        self.version_input = QLineEdit()
        self.description_input = QLineEdit()
        
        layout.addRow("Name:", self.name_input)
        layout.addRow("Vendor:", self.vendor_input)
        layout.addRow("Model:", self.model_input)
        layout.addRow("Version:", self.version_input)
        layout.addRow("Description:", self.description_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save_device)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
        self.load_device()
    
    def load_device(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, vendor, model, version, description FROM devices WHERE mac = ?", (self.device_mac,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            self.name_input.setText(result[0] or "")
            self.vendor_input.setText(result[1] or "")
            self.model_input.setText(result[2] or "")
            self.version_input.setText(result[3] or "")
            self.description_input.setText(result[4] or "")
    
    def save_device(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE devices SET name=?, vendor=?, model=?, version=?, description=?
            WHERE mac=?
        """, (
            self.name_input.text(),
            self.vendor_input.text(),
            self.model_input.text(),
            self.version_input.text(),
            self.description_input.text(),
            self.device_mac
        ))
        conn.commit()
        conn.close()
        self.accept()

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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["IP Address", "IPv6", "MAC Address", "Vendor", "Last Seen"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.doubleClicked.connect(self.edit_device)
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
            self.table.setItem(row, 1, QTableWidgetItem(device.get("ipv6", "N/A")))
            self.table.setItem(row, 2, QTableWidgetItem(device["mac"]))
            self.table.setItem(row, 3, QTableWidgetItem(device["vendor"]))
            self.table.setItem(row, 4, QTableWidgetItem(device["last_seen"]))
        self.scan_button.setText("Scan Network")
        self.scan_button.setEnabled(True)
        
    def edit_device(self, index):
        row = index.row()
        mac = self.table.item(row, 1)
        if mac:
            dialog = EditDeviceDialog(mac.text(), self)
            dialog.exec_()    
            
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = DevicesTab()
    window.show()
    sys.exit(app.exec_())