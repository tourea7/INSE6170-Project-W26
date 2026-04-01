from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QSpinBox, QLineEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.capture import start_capture


class CaptureTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("Packet Capture")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        mac_layout = QHBoxLayout()
        mac_layout.addWidget(QLabel("Device MAC Address:"))
        self.mac_input = QLineEdit()
        self.mac_input.setPlaceholderText("eg: 16:2d:4d:de:e7:64")
        mac_layout.addWidget(self.mac_input)
        layout.addLayout(mac_layout)
        
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Filename:"))
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("eg: capture1.pcap")
        file_layout.addWidget(self.file_input)
        layout.addLayout(file_layout)
        
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Packet Count:"))
        self.count_input = QSpinBox()
        self.count_input.setMinimum(1)
        self.count_input.setMaximum(10000)
        self.count_input.setValue(100)
        count_layout.addWidget(self.count_input)
        layout.addLayout(count_layout)
        
        btn_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Capture")
        self.start_button.clicked.connect(self.start_capture)
        self.stop_button = QPushButton("Stop Capture")
        self.stop_button.setEnabled(False)
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.stop_button)
        layout.addLayout(btn_layout)
        
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        
    def start_capture(self):
        mac = self.mac_input.text()
        filename =self.file_input.text()
        count = self.count_input.value()
        
        if not mac or not filename: 
            self.status_label.setText("Status: Please enter MAC address and  filename")
            return
        self.status_label.setText(f"Status: Capturing {count} packets from {mac}... ")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        filepath = start_capture(mac, filename, count)
        
        self.status_label.setText(f"Status: Capture saved to {filepath}")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = CaptureTab()
    window.show()
    sys.exit(app.exec_())        

            