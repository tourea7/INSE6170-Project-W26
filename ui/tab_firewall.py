from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox
from core.firewall import add_rule, get_rules, apply_firewall_rules, remove_firewall_rules, start_scapy_firewall, stop_scapy_firewall
import sys
import os
from core.firewall import add_rule, get_rules, apply_firewall_rules, remove_firewall_rules
import sqlite3
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db')

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PyQt5.QtCore import QThread, pyqtSignal

class FirewallWorker(QThread):
    def run(self):
        start_scapy_firewall()


class FirewallTab(QWidget): #classe pour gérer les règles de pare-feu dans l'interface utilisateur
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("🛡  Firewall Rules")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; color: #a78bfa;")
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
        

        protocol_layout = QHBoxLayout()
        protocol_layout.addWidget(QLabel("Protocol:"))
        self.protocol_input = QComboBox()
        self.protocol_input.addItems(["TCP", "UDP"])
        protocol_layout.addWidget(self.protocol_input)
        layout.addLayout(protocol_layout)
        
        btn_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Rule")
        self.add_button.clicked.connect(self.add_rule)
        self.load_button = QPushButton("Load Rules")
        self.load_button.clicked.connect(self.load_rules)
        self.apply_button = QPushButton("Apply Firewall")
        self.apply_button.clicked.connect(self.apply_rules)
        self.remove_button = QPushButton("Remove Firewall")
        self.remove_button.clicked.connect(self.remove_rules)
        self.delete_rule_button = QPushButton("Delete Selected Rule")
        self.delete_rule_button.clicked.connect(self.delete_selected_rule)
        self.start_fw_button = QPushButton("▶ Start Firewall")
        self.start_fw_button.clicked.connect(self.start_firewall)
        self.stop_fw_button = QPushButton("⏹ Stop Firewall")
        self.stop_fw_button.clicked.connect(self.stop_firewall)
        self.stop_fw_button.setEnabled(False)
        btn_layout.addWidget(self.start_fw_button)
        btn_layout.addWidget(self.stop_fw_button)
        btn_layout.addWidget(self.load_button)
        btn_layout.addWidget(self.apply_button)
        btn_layout.addWidget(self.remove_button)
        btn_layout.addWidget(self.delete_rule_button)
        btn_layout.addWidget(self.add_button)
        layout.addLayout(btn_layout)
        
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Device MAC", "Allowed IP", "Port", "Protocol"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def start_firewall(self):
        from PyQt5.QtCore import QThread
        self.fw_thread = QThread()
        self.fw_worker = FirewallWorker()
        self.fw_worker.moveToThread(self.fw_thread)
        self.fw_thread.started.connect(self.fw_worker.run)
        self.fw_thread.start()
        self.start_fw_button.setEnabled(False)
        self.stop_fw_button.setEnabled(True)
        self.status_label.setText("Status: Scapy firewall running...")

    def stop_firewall(self):
        stop_scapy_firewall()
        self.start_fw_button.setEnabled(True)
        self.stop_fw_button.setEnabled(False)
        self.status_label.setText("Status: Firewall stopped")    
        
    def add_rule(self):
        mac = self.mac_input.text()
        ip = self.ip_input.text()
        port = self.port_input.value()
        
        if not mac or not ip:
            self.status_label.setText("Status: Please enter MAC address and IP")
            return
        
        add_rule(mac, ip, port, self.protocol_input.currentText())
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
            self.table.setItem(row, 0, QTableWidgetItem(mac))
            self.table.setItem(row, 1, QTableWidgetItem(rule[0]))
            self.table.setItem(row, 2, QTableWidgetItem(str(rule[1])))
            self.table.setItem(row, 3, QTableWidgetItem(rule[2]))
            
        self.status_label.setText(f"Status: {len(rules)} rules loaded")
        
    def apply_rules(self):
        mac = self.mac_input.text()
        if not mac:
            self.status_label.setText("Status: Please enter MAC address")
            return
        apply_firewall_rules(mac)
        self.status_label.setText(f"Status: Firewall rules applied for {mac}")
    
    def remove_rules(self):
        mac = self.mac_input.text()
        if not mac:
            self.status_label.setText("Status: Please enter MAC address")
            return
        remove_firewall_rules(mac)
        self.status_label.setText(f"Status: Firewall rules removed for {mac}") 
        
    def delete_selected_rule(self):
        selected = self.table.currentRow()
        if selected < 0:
            self.status_label.setText("Status: Please select a rule")
            return
        mac = self.table.item(selected, 0).text()
        ip = self.table.item(selected, 1).text()
        port = self.table.item(selected, 2).text()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM firewall_rules WHERE device_mac=? AND allowed_ip=? AND allowed_port=?", 
                      (mac, ip, int(port)))
        conn.commit()
        conn.close()
        self.table.removeRow(selected)
        self.status_label.setText(f"Status: Rule deleted")       

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = FirewallTab()
    window.show()
    sys.exit(app.exec_())            