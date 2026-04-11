from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import qtawesome as qta
import sys

from tab_devices import DevicesTab
from tab_capture import CaptureTab
from tab_firewall import FirewallTab
from tab_ips import IPSTab
from tab_logs import LogsTab

class StatCard(QFrame):
    def __init__(self, icon, title, value, color):
        super().__init__()
        self.setFixedHeight(70)
        self.setObjectName("statcard")
        self.setStyleSheet(
            "QFrame#statcard {"
            "background-color: white;"
            "border-radius: 8px;"
            f"border-left: 4px solid {color};"
            "}"
        )
        layout = QHBoxLayout()
        layout.setContentsMargins(12, 8, 12, 8)
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon, color=color).pixmap(18, 18))
        icon_label.setFixedSize(22, 22)
        layout.addWidget(icon_label)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {color}; border: none;")
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 10px; color: #888888; border: none;")
        text_layout.addWidget(self.value_label)
        text_layout.addWidget(self.title_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart IoT Router")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f2f5; }
            QTabWidget::pane { border: 1px solid #cccccc; background-color: #ffffff; }
            QTabBar::tab { background-color: #2c3e50; color: white; padding: 8px 20px; margin-right: 2px; border-radius: 4px 4px 0 0; font-size: 13px; min-width: 100px; }
            QTabBar::tab:selected { background-color: #2980b9; color: white; }
            QPushButton { background-color: #2980b9; color: white; padding: 8px 16px; border-radius: 6px; font-size: 13px; border: none; max-width: 200px; }
            QPushButton:hover { background-color: #3498db; }
            QPushButton:disabled { background-color: #95a5a6; }
            QTableWidget { gridline-color: #e0e0e0; font-size: 12px; border: 1px solid #cccccc; }
            QHeaderView::section { background-color: #2c3e50; color: white; padding: 8px; font-size: 12px; border: none; }
            QLabel { font-size: 13px; color: #2c3e50; }
            QLineEdit, QSpinBox { padding: 6px; border: 1px solid #cccccc; border-radius: 4px; font-size: 13px; }
            QLineEdit:focus, QSpinBox:focus { border: 1px solid #2980b9; }
        """)

        central = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Stats cards
        stats_layout = QHBoxLayout()
        self.card_devices = StatCard("fa5s.network-wired", "Devices Connected", "0", "#2980b9")
        self.card_traffic = StatCard("fa5s.chart-line", "Total Traffic", "0 KB", "#27ae60")
        self.card_alerts = StatCard("fa5s.exclamation-triangle", "Active Alerts", "0", "#e74c3c")
        self.card_firewall = StatCard("fa5s.shield-alt", "Firewall Rules", "0", "#8e44ad")
        stats_layout.addWidget(self.card_devices)
        stats_layout.addWidget(self.card_traffic)
        stats_layout.addWidget(self.card_alerts)
        stats_layout.addWidget(self.card_firewall)
        main_layout.addLayout(stats_layout)

        # Tabs
        self.tabs = QTabWidget()
        self.tab_devices = DevicesTab()
        self.tab_capture = CaptureTab()
        self.tab_firewall = FirewallTab()
        self.tab_ips = IPSTab()
        self.tab_logs = LogsTab()

        self.tabs.addTab(self.tab_devices, qta.icon("fa5s.network-wired", color="white"), "Devices")
        self.tabs.addTab(self.tab_capture, qta.icon("fa5s.file-download", color="white"), "Packet Capture")
        self.tabs.addTab(self.tab_firewall, qta.icon("fa5s.shield-alt", color="white"), "Firewall")
        self.tabs.addTab(self.tab_ips, qta.icon("fa5s.exclamation-triangle", color="white"), "IPS")
        self.tabs.addTab(self.tab_logs, qta.icon("fa5s.chart-bar", color="white"), "Logs")

        main_layout.addWidget(self.tabs)
        central.setLayout(main_layout)
        self.setCentralWidget(central)
     
    def update_stats(self, devices=None, alerts=0, rules=0):
        if devices is not None:
            self.card_devices.value_label.setText(str(len(devices)))
        self.card_alerts.value_label.setText(str(alerts))
        self.card_firewall.value_label.setText(str(rules))
        
    def on_device_selected(self, mac, ip):
        self.tab_capture.mac_input.setText(mac)
        

        self.tab_ips.mac_input.setText(mac)
        self.tab_ips.ip_input.setText(ip)
        
        
        self.tab_firewall.mac_input.setText(mac)        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())