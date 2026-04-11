from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QSpinBox
from PyQt5.QtCore import Qt
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import glob
import sqlite3
import datetime
from PyQt5.QtWidgets import QScrollArea

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db')

class LogsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Logs and History")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Days input
        days_layout = QHBoxLayout()
        days_layout.addWidget(QLabel("Show last (days):"))
        self.days_input = QSpinBox()
        self.days_input.setMinimum(1)
        self.days_input.setMaximum(365)
        self.days_input.setValue(7)
        days_layout.addWidget(self.days_input)
        layout.addLayout(days_layout)
        
        # History buttons
        btn_layout = QHBoxLayout()
        self.load_button = QPushButton("Load History")
        self.load_button.clicked.connect(self.load_history)
        self.delete_button = QPushButton("Delete All Records")
        self.delete_button.clicked.connect(self.delete_records)
        btn_layout.addWidget(self.load_button)
        btn_layout.addWidget(self.delete_button)
        layout.addLayout(btn_layout)
        
        # History table
        self.table = QTableWidget()
        self.table.setFixedHeight(120)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Device MAC", "Timestamp", "Data Rate (KB/s)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 180)
        layout.addWidget(self.table)
        
        # Status
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)
        
        
        self.plot_button = QPushButton("Show Graph")
        self.plot_button.clicked.connect(self.show_graph)
        layout.addWidget(self.plot_button)
        
        # Graph
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedHeight(250)
        layout.addWidget(self.canvas)
        
        # Separator
        line = QLabel("")
        line.setStyleSheet("border-top: 1px solid #cccccc; margin: 5px 0;")
        layout.addWidget(line)
        
        # PCAP section
        pcap_title = QLabel("PCAP Files")
        pcap_title.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(pcap_title)
        
        pcap_btn_layout = QHBoxLayout()
        self.load_pcap_button = QPushButton("Load PCAP Files")
        self.load_pcap_button.clicked.connect(self.load_pcap_files)
        self.delete_pcap_button = QPushButton("Delete Selected PCAP")
        self.delete_pcap_button.clicked.connect(self.delete_pcap_file)
        pcap_btn_layout.addWidget(self.load_pcap_button)
        pcap_btn_layout.addWidget(self.delete_pcap_button)
        layout.addLayout(pcap_btn_layout)
        
        self.pcap_table = QTableWidget()
        self.pcap_table.setColumnCount(3)
        self.pcap_table.setHorizontalHeaderLabels(["Filename", "Size", "Created"])
        self.pcap_table.horizontalHeader().setStretchLastSection(True)
        self.pcap_table.setFixedHeight(120)
        layout.addWidget(self.pcap_table)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
    def load_history(self):
        days = self.days_input.value()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT device_mac, timestamp, data_rate 
            FROM bandwidth_history 
            WHERE timestamp >= datetime('now', ?)
            ORDER BY timestamp DESC
        """, (f'-{days} days',))
        
        records = cursor.fetchall()
        conn.close()
        
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(record[0]))
            self.table.setItem(row, 1, QTableWidgetItem(record[1]))
            self.table.setItem(row, 2, QTableWidgetItem(str(round(record[2], 2))))
        
        self.status_label.setText(f"Status: {len(records)} records found")
        self.show_graph()
    
    def delete_records(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bandwidth_history")
        conn.commit()
        conn.close()
        
        self.table.setRowCount(0)
        self.status_label.setText("Status: All records deleted")    
        
        
    def show_graph(self):
        days = self.days_input.value()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT timestamp, data_rate 
            FROM bandwidth_history 
            WHERE timestamp >= datetime('now', ?)
            ORDER BY timestamp ASC
        """, (f'-{days} days',))
        
        records = cursor.fetchall()
        conn.close()
        
        if not records:
            self.status_label.setText("Status: No data to display")
            return
        
        timestamps = [r[0] for r in records]
        rates = [r[1] for r in records]
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(rates, color='blue', linewidth=1.5)
        ax.set_title("Bandwidth History")
        ax.set_ylabel("Data Rate (KB/s)")
        ax.set_xlabel("Time")
        ax.grid(True)
        
        self.canvas.draw()
        self.status_label.setText(f"Status: Graph updated with {len(records)} records")    

    def load_pcap_files(self):
        pcap_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'pcap')
        files = glob.glob(os.path.join(pcap_folder, '*.pcap'))
        
        self.pcap_table.setRowCount(len(files))
        for row, filepath in enumerate(files):
            filename = os.path.basename(filepath)
            size = f"{os.path.getsize(filepath)} bytes"
            created = datetime.datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
            self.pcap_table.setItem(row, 0, QTableWidgetItem(filename))
            self.pcap_table.setItem(row, 1, QTableWidgetItem(size))
            self.pcap_table.setItem(row, 2, QTableWidgetItem(created))
        
        self.status_label.setText(f"Status: {len(files)} pcap files found")
    
    def delete_pcap_file(self):
        selected = self.pcap_table.currentRow()
        if selected < 0:
            self.status_label.setText("Status: Please select a file to delete")
            return
        
        filename = self.pcap_table.item(selected, 0).text()
        pcap_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'pcap')
        filepath = os.path.join(pcap_folder, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            self.pcap_table.removeRow(selected)
            self.status_label.setText(f"Status: {filename} deleted")
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = LogsTab()
    window.show()
    sys.exit(app.exec_())        