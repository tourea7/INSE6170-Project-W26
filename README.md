# INSE6170-Project-W26
================================================================
IoT Shield — Real-time IoT Network Monitoring and Security
INSE 6170 — Network Security Architecture and Management
Concordia University — Winter 2026
Student: Aicha Yasmine Toure - 40327421
GitHub: https://github.com/tourea7/INSE6170-Project-W26
================================================================

DESCRIPTION
-----------
IoT Shield is a desktop application developed in Python
that transforms a PC into a smart wireless router for
IoT device monitoring and security. It implements five
core functions: device discovery, packet capture,
whitelist-based firewall, intrusion prevention (IPS),
and log management.

REQUIREMENTS
------------
- Windows 10 or later
- Python 3.11 or later
- Administrator privileges (required for Scapy and netsh)
- WiFi adapter (to create the PC hotspot)

INSTALLATION
------------
Step 1 — Install Python 3.11+
   Download from: https://www.python.org/downloads/
   IMPORTANT: Check "Add Python to PATH" during installation

Step 2 — Install Npcap
   Download from: https://npcap.com
   Check "Install Npcap in WinPcap API-compatible mode"

Step 3 — Install required libraries
   Open a terminal and run:
   pip install scapy psutil PyQt5 matplotlib requests qtawesome

RUNNING THE APPLICATION
-----------------------
Option 1 (Recommended):
   Double-click launch_admin.bat
   This automatically requests administrator rights.

Option 2 (Manual):
   Open cmd as Administrator
   Navigate to the project folder:
   cd C:\path\to\INSE6170-Project-W26
   Run:
   python main.py

NETWORK SETUP
-------------
1. Activate the hotspot on your phone
2. Connect your PC to the phone hotspot
3. Connect your IoT devices to the same hotspot
4. Launch IoT Shield
5. Click "Scan Network" to detect connected devices

FIND YOUR NETWORK RANGE
------------------------
Open cmd and type: ipconfig
Look for your WiFi adapter
Example: IP 192.168.1.5 → network is 192.168.1.0/24
Update network range in core/scanner.py

FILE STRUCTURE
--------------
INSE6170-Project-W26/
├── main.py                  → Application entry point
├── launch_admin.bat         → Launch with admin rights
├── check_db.py              → Database inspection tool
├── core/
│   ├── scanner.py           → ARP device discovery
│   ├── capture.py           → Packet capture
│   ├── firewall.py          → Firewall management
│   ├── ips.py               → Intrusion prevention
│   └── database.py          → SQLite database
├── ui/
│   ├── main_window.py       → Main application window
│   ├── tab_devices.py       → Devices tab
│   ├── tab_capture.py       → Packet capture tab
│   ├── tab_firewall.py      → Firewall tab
│   ├── tab_ips.py           → IPS tab
│   └── tab_logs.py          → Logs tab
└── data/
    ├── devices.db           → SQLite database
    └── pcap/                → Captured packet files

GMAIL ALERT CONFIGURATION
--------------------------
To receive email alerts from the IPS:
1. Go to myaccount.google.com/apppasswords
2. Generate an App Password for "IoT Shield"
3. In core/ips.py, replace APP_PASSWORD with your password
4. Update alert_email with your Gmail address

NOTES
-----
- The application must be run as Administrator
- Scapy requires Npcap to capture packets on Windows
- The firewall functions use Windows Defender Firewall
- All data is stored locally in data/devices.db

================================================================