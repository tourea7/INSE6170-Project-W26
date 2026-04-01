from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpinBox
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.ips import start_monitoring, stop_monitoring

class IPSTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
    
        title = QLabel("Intrusion Prevention System")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("Device IP:"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("e.g. 172.20.10.1")
        ip_layout.addWidget(self.ip_input)
        layout.addLayout(ip_layout)
        
   
        mac_layout = QHBoxLayout()
        mac_layout.addWidget(QLabel("Device MAC:"))
        self.mac_input = QLineEdit()
        self.mac_input.setPlaceholderText("e.g. 16:2d:4d:de:e7:64")
        mac_layout.addWidget(self.mac_input)
        layout.addLayout(mac_layout)
        
   
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("Max rate (KB/s):"))
        self.rate_input = QSpinBox()
        self.rate_input.setMinimum(1)
        self.rate_input.setMaximum(100000)
        self.rate_input.setValue(100)
        rate_layout.addWidget(self.rate_input)
        layout.addLayout(rate_layout)
        
     
        min_layout = QHBoxLayout()
        min_layout.addWidget(QLabel("Throttle duration (minutes):"))
        self.min_input = QSpinBox()
        self.min_input.setMinimum(1)
        self.min_input.setMaximum(60)
        self.min_input.setValue(5)
        min_layout.addWidget(self.min_input)
        layout.addLayout(min_layout)
        
      
        btn_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Monitoring")
        self.start_button.clicked.connect(self.start_monitoring)
        self.stop_button = QPushButton("Stop Monitoring")
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.stop_button)
        layout.addLayout(btn_layout)
        
    
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
        
    def start_monitoring(self):
        ip = self.ip_input.text()
        mac = self.mac_input.text()
        max_rate = self.rate_input.value()
        n_minutes = self.min_input.value()
        
        if not ip or not mac:
            self.status_label.setText("Status: Please enter IP and MAC address")
            return
        
        start_monitoring(ip, mac, max_rate, n_minutes)
        self.status_label.setText(f"Status: Monitoring {ip} (max {max_rate} KB/s)")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
    
    def stop_monitoring(self):
        stop_monitoring()
        self.status_label.setText("Status: Monitoring stopped")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)    
        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = IPSTab()
    window.show()
    sys.exit(app.exec_())        