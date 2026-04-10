from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QSpinBox
from PyQt5.QtCore import Qt
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db')

class LogsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
       
        title = QLabel("Logs and History")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
      
        days_layout = QHBoxLayout()
        days_layout.addWidget(QLabel("Show last (days):"))
        self.days_input = QSpinBox()
        self.days_input.setMinimum(1)
        self.days_input.setMaximum(365)
        self.days_input.setValue(7)
        days_layout.addWidget(self.days_input)
        layout.addLayout(days_layout)
  
        btn_layout = QHBoxLayout()
        self.load_button = QPushButton("Load History")
        self.load_button.clicked.connect(self.load_history)
        self.delete_button = QPushButton("Delete All Records")
        self.delete_button.clicked.connect(self.delete_records)
        btn_layout.addWidget(self.load_button)
        btn_layout.addWidget(self.delete_button)
        layout.addLayout(btn_layout)
    
        self.table = QTableWidget()
        self.table.setMinimumHeight(150)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Device MAC", "Timestamp", "Data Rate (KB/s)"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
  
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(200)
        layout.addWidget(self.canvas)
        
        self.plot_button = QPushButton("Show Graph")
        self.plot_button.clicked.connect(self.show_graph)
        layout.addWidget(self.plot_button)
        
        self.setLayout(layout)
        
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
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = LogsTab()
    window.show()
    sys.exit(app.exec_())        