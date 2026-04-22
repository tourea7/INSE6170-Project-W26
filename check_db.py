import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'devices.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 60)
print("DEVICES TABLE")
print("=" * 60)
cursor.execute("SELECT id, ip, mac, vendor, name, model FROM devices")
for row in cursor.fetchall():
    print(row)

print("\n" + "=" * 60)
print("FIREWALL RULES TABLE")
print("=" * 60)
cursor.execute("SELECT * FROM firewall_rules")
for row in cursor.fetchall():
    print(row)

print("\n" + "=" * 60)
print("BANDWIDTH HISTORY (last 10)")
print("=" * 60)
cursor.execute("SELECT device_mac, timestamp, data_rate FROM bandwidth_history ORDER BY id DESC LIMIT 10")
for row in cursor.fetchall():
    print(row)

print("\n" + "=" * 60)
print("ALERTS TABLE")
print("=" * 60)
cursor.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 5")
for row in cursor.fetchall():
    print(row)

print("\n" + "=" * 60)
print("PCAP FILES")
print("=" * 60)
pcap_folder = os.path.join(os.path.dirname(__file__), 'data', 'pcap')
if os.path.exists(pcap_folder):
    files = os.listdir(pcap_folder)
    for f in files:
        print(f)

conn.close()
print("\nDone!")