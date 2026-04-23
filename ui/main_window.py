from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFont, QFontDatabase
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
            "background-color: #161b22;"
            "border-radius: 8px;"
            f"border-left: 4px solid {color};"
            "border: 1px solid #30363d;"
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
        self.value_label.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {color}; background: transparent; border: none;")
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 11px; color: #6e7681; background: transparent; border: none;")
        text_layout.addWidget(self.value_label)
        text_layout.addWidget(self.title_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛡 IoT Shield")
        self.setMinimumSize(1100, 700)
        self.resize(1100, 700)
        QApplication.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("""
            QMainWindow { background-color: #0d1117; }
            QWidget { background-color: #0d1117; color: #e6edf3; }
            QTabWidget::pane { border: 1px solid #30363d; background-color: #161b22; }
            QTabBar::tab { background-color: #161b22; color: #8b949e; padding: 8px 20px; margin-right: 2px; border-radius: 4px 4px 0 0; font-size: 13px; min-width: 100px; border: 1px solid #30363d; }
            QTabBar::tab:selected { background-color: #7c3aed; color: white; border: 1px solid #7c3aed; }
            QTabBar::tab:hover { background-color: #21262d; color: white; }
            QPushButton { background-color: #7c3aed; color: white; padding: 8px 16px; border-radius: 6px; font-size: 13px; border: none; max-width: 200px; }
            QPushButton:hover { background-color: #8b5cf6; }
            QPushButton:disabled { background-color: #21262d; color: #484f58; }
            QTableWidget { background-color: #161b22; gridline-color: #30363d; font-size: 12px; border: 1px solid #30363d; color: #e6edf3; }
            QTableWidget::item { padding: 4px; }
            QTableWidget::item:selected { background-color: #7c3aed; }
            QHeaderView::section { background-color: #21262d; color: #8b949e; padding: 8px; font-size: 12px; border: none; border-bottom: 1px solid #30363d; }
            QLabel { font-size: 13px; color: #e6edf3; }
            QLineEdit, QSpinBox { background-color: #21262d; padding: 6px; border: 1px solid #30363d; border-radius: 4px; font-size: 13px; color: #e6edf3; }
            QLineEdit:focus, QSpinBox:focus { border: 1px solid #7c3aed; }
            QScrollArea { border: none; background-color: #0d1117; }
            QFormLayout { background-color: #161b22; }
            QDialog { background-color: #161b22; color: #e6edf3; }
        """)
        central = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)
        
        main_layout.setSpacing(12)

        # Header with logo
        header_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_label.setPixmap(qta.icon("fa5s.shield-alt", color="#a78bfa").pixmap(70, 70))
        logo_label.setFixedSize(80, 80)
        title_layout = QVBoxLayout()
        app_title = QLabel("IoT SHIELD")
        app_title.setStyleSheet("font-size: 42px; font-weight: 900; color: #a78bfa; letter-spacing: 4px; background: transparent;")
        app_subtitle = QLabel("Real-time IoT Network Monitoring")
        app_subtitle.setStyleSheet("font-size: 13px; color: #9ca3af; letter-spacing: 1px; background: transparent;")
        title_layout.addWidget(app_title)
        title_layout.addWidget(app_subtitle)
        title_layout.setSpacing(2)
        header_layout.setSpacing(12)
        header_layout.addWidget(logo_label)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        

        # Stats cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)
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
        from PyQt5.QtCore import QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_stats)
        self.timer.start(5000)
     
    def update_stats(self, devices=None, alerts=0, rules=0):
        if devices is not None:
            self.card_devices.value_label.setText(str(len(devices)))
        
        # Count firewall rules
        try:
            import sqlite3
            import os
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM firewall_rules")
            rule_count = cursor.fetchone()[0]
            conn.close()
            self.card_firewall.value_label.setText(str(rule_count))
        except:
            pass
        # Count active alerts
        try:
            cursor.execute("SELECT COUNT(*) FROM alerts WHERE timestamp >= datetime('now', '-1 day')")
            alert_count = cursor.fetchone()[0]
            conn.close()
            self.card_alerts.value_label.setText(str(alert_count))
            if alert_count > 0:
                self.card_alerts.setStyleSheet(
                    "QFrame#statcard {"
                    "background-color: #fde8e8;"
                    "border-radius: 8px;"
                    "border-left: 4px solid #e74c3c;"
                    "}"
                )
        except:
            pass
        
    def on_device_selected(self, mac, ip):
        self.tab_capture.mac_input.setText(mac)
        

        self.tab_ips.mac_input.setText(mac)
        self.tab_ips.ip_input.setText(ip)
        
        
        self.tab_firewall.mac_input.setText(mac)     
        
    def refresh_stats(self):
        try:
            import sqlite3
            import os
            import psutil
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM firewall_rules")
            self.card_firewall.value_label.setText(str(cursor.fetchone()[0]))
            
            cursor.execute("SELECT COUNT(*) FROM alerts WHERE timestamp >= datetime('now', '-1 day')")
            alert_count = cursor.fetchone()[0]
            self.card_alerts.value_label.setText(str(alert_count))
            if alert_count > 0:
                self.card_alerts.setStyleSheet(
                    "QFrame#statcard {"
                    "background-color: #fde8e8;"
                    "border-radius: 8px;"
                    "border-left: 4px solid #e74c3c;"
                    "}"
                )
            
            net = psutil.net_io_counters()
            total_bytes = net.bytes_sent + net.bytes_recv
            if total_bytes > 1024 * 1024 * 1024:
                self.card_traffic.value_label.setText(f"{total_bytes / (1024**3):.1f} GB")
            elif total_bytes > 1024 * 1024:
                self.card_traffic.value_label.setText(f"{total_bytes / (1024**2):.1f} MB")
            else:
                self.card_traffic.value_label.setText(f"{total_bytes / 1024:.1f} KB")
            
            conn.close()
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())