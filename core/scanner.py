from scapy.all import ARP , Ether , srp
import datetime
import requests
import sqlite3
import os
import subprocess


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db')

def scan_networks(network="172.20.10.0/28"):
    """Scans the specified networks and returns a list of active devices."""
    print(f"Scanning network: {network}...")
    
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    
    result = srp(packet, timeout=3, verbose=0)[0]
    
    devices = []
    for sent, received in result:
        device = {
            "ip":received.psrc,
            "mac": received.hwsrc,
            "vendor" : get_vendor(received.hwsrc),
            "last_seen": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        }
        devices.append(device)
        save_device(device)
        
    return devices
def get_vendor(mac):
    """Find te vendor of the device using its MAC address."""
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
        return "Unknown"
    except :
        return "Unknown"
    
def get_ipv6(ip):
    """Get IPv6 address of a device using ping6"""
    try:
        result = subprocess.run(
            ["ping", "-6", "-n", "1", ip],
            capture_output=True, text=True, timeout=3
        )
        for line in result.stdout.split('\n'):
            if 'Reply from' in line:
                parts = line.split()
                for part in parts:
                    if ':' in part and part.count(':') > 1:
                        return part.rstrip(':')
        return "N/A"
    except:
        return "N/A"
    
def save_device(device):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO devices (ip, mac, vendor, last_seen)
        VALUES (?, ?, ?, ?)
    """, (device["ip"], device["mac"], device["vendor"], device["last_seen"]))
    
    conn.commit()
    conn.close()    
    
if __name__ == "__main__":
    devices = scan_networks()
    print(f"\n{len(devices)} devices found:")
    for d in devices:
        print(f"IP: {d['ip']} MAC: {d['mac']} Vendor: {d['vendor']}")
        