from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QSpinBox
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.firewall import add_rule, get_rules

class FirewallTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("Firewall Rules")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        mac_layout = QHBoxLayout()
        mac_layout.addWidget(QLabel("Device MAC:"))
        self.mac_input = QLineEdit()
        self.mac_input.setPlaceholderText("eg: 16:2d:4d:de:e7:64")
        mac_layout.addWidget(self.mac_input)
        layout.addLayout(mac_layout)

        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("Allowed IP:"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("eg: 192.168.1.1")
        ip_layout.addWidget(self.ip_input)
        layout.addLayout(ip_layout)
        
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Allowed Port:"))
        self.port_input = QSpinBox()
        self.port_input.setMinimum(1)
        self.port_input.setMaximum(65535)
        self.port_input.setValue(443)
        port_layout.addWidget(self.port_input)
        layout.addLayout(port_layout)
        
        btn_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Rule")
        self.add_button.clicked.connect(self.add_rule)
        self.load_button = QPushButton("Load Rules")
        self.load_button.clicked.connect(self.load_rules)
        btn_layout.addWidget(self.add_button)
        btn_layout.addWidget(self.load_button)
        layout.addWidget(self.add_button)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Device MAC", "Allowed IP", "Port", "Protocol"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def add_rule(self):
        mac = self.mac_input.text()
        ip = self.ip_input.text()
        port = self.port_input.value()
        
        if not mac or not ip:
            self.status_label.setText("Status: Please enter MAC address and IP")
            return
        
        add_rule(mac, ip, port)
        self.status_label.setText(f"Status: Rule added for {mac} to allow {ip}:{port}")
        self.load_rules()
        
    def load_rules(self):
        mac = self.mac_input.text()
        
        if not mac:
            self.status_label.setText("Status: Please enter MAC address")
            return
        
        rules = get_rules(mac)
        self.table.setRowCount(len(rules))
        
        for row, rule in enumerate(rules):
            self.table.setItem(row, 0, QTableWidgetItem(rule[mac]))
            self.table.setItem(row, 1, QTableWidgetItem(rule[0]))
            self.table.setItem(row, 2, QTableWidgetItem(str(rule[1])))
            self.table.setItem(row, 3, QTableWidgetItem(rule[2]))
            
        self.status_label.setText(f"Status: {len(rules)} rules loaded")
        
        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = FirewallTab()
    window.show()
    sys.exit(app.exec_())            