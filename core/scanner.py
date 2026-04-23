from scapy.all import ARP , Ether , srp
import datetime
import requests
import sqlite3
import os
import subprocess


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db')

#par défaut, on scanne un petit réseau local pour éviter les problèmes de temps d'attente et de permissions. Vous pouvez ajuster ce paramètre selon vos besoins.
def scan_networks(network="172.20.10.0/28"): 
    """Scans the specified networks and returns a list of active devices."""
    print(f"Scanning network: {network}...")
    
    arp = ARP(pdst=network) #crée un paquet ARP pour tout le réseau
    ether = Ether(dst="ff:ff:ff:ff:ff:ff") # broadcast à tous les appareils
    packet = ether/arp #combine les deux paquets pour créer un paquet complet à envoyer
    result = srp(packet, timeout=3, verbose=0)[0] #envoie et reçoit les réponses
    
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
def get_vendor(mac): # fonction pour obtenir le fabricant à partir de l'adresse MAC en utilisant une API publique
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
    """Get IPv6 address using Windows arp/netsh command"""
    try:
        result = subprocess.run(
            ["netsh", "interface", "ipv6", "show", "neighbors"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.split('\n'):
            if ip in line and ':' in line:
                parts = line.split()
                for part in parts:
                    if ':' in part and len(part) > 8:
                        return part
        return "N/A"
    except:
        return "N/A"
    
def save_device(device): #fonction pour sauvegarder les informations de l'appareil dans la base de données SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO devices (ip, mac, vendor, last_seen)
        VALUES (?, ?, ?, ?)
    """, (device["ip"], device["mac"], device["vendor"], device["last_seen"]))
    
    conn.commit()
    conn.close()    
    
if __name__ == "__main__": #test de la fonction de scan
    devices = scan_networks()
    print(f"\n{len(devices)} devices found:")
    for d in devices:
        print(f"IP: {d['ip']} MAC: {d['mac']} Vendor: {d['vendor']}")
        