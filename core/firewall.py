from scapy.all import sniff, IP, TCP, UDP
import sqlite3
import os
import subprocess

DB_PATH = os.path.join(os.path.dirname(__file__),'..', 'data', 'devices.db')

def get_rules(device_mac):
    #connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    #fetch rules for this devices 
    cursor.execute("SELECT allowed_ip, allowed_port, protocol FROM firewall_rules WHERE device_mac = ?" , (device_mac,))
    rules = cursor.fetchall()
    
    conn.close()
    return rules

def is_allowed(packet, rules):
    #if no rules, block all traffic
    if not rules:
        return False
    
    #check if packet matches any rules
    for allowed_ip, allowed_port, protocol in rules:
        if IP in packet:
            if packet [IP].dst == allowed_ip:
                if TCP in packet and packet[TCP].dport == allowed_port:
                    return True
                if UDP in packet and packet [UDP].dport == allowed_port:
                    return True
    return False

def add_rule(device_mac, allowed_ip, allowed_port, protocol="TCP"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
                   INSERT INTO firewall_rules (device_mac, allowed_ip, allowed_port, protocol)
                   VALUES (?, ?, ?, ?)
                   """, (device_mac, allowed_ip, allowed_port, protocol))
    conn.commit()
    conn.close()
    print(f"Rule added: {device_mac} -> {allowed_ip}:{allowed_port} ({protocol})")
    
 
def apply_firewall_rules(device_mac):
    """Apply whitelist rules using Windows Firewall"""
    rules = get_rules(device_mac)
    
    # First block all traffic from this device
    subprocess.run([
        "netsh", "advfirewall", "firewall", "add", "rule",
        f"name=block_all_{device_mac.replace(':', '-')}",
        "protocol=TCP",
        "dir=in",
        "action=block",
        "enable=yes"
    ], capture_output=True)
    
    # Then allow only whitelisted traffic
    for rule in rules:
        allowed_ip, allowed_port, protocol = rule
        subprocess.run([
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name=allow_{device_mac.replace(':', '-')}_{allowed_ip}_{allowed_port}",
            f"protocol={protocol}",
            "dir=in",
            f"remoteip={allowed_ip}",
            f"localport={allowed_port}",
            "action=allow",
            "enable=yes"
        ], capture_output=True)
        print(f"Rule applied: allow {allowed_ip}:{allowed_port} ({protocol})")
    
    print(f"Firewall rules applied for {device_mac}")

def remove_firewall_rules(device_mac):
    """Remove all firewall rules for a device"""
    subprocess.run([
        "netsh", "advfirewall", "firewall", "delete", "rule",
        f"name=block_all_{device_mac.replace(':', '-')}"
    ], capture_output=True)
    print(f"Firewall rules removed for {device_mac}")
    
        
def start_firewall(device_mac):
        print(f"Firewall started for {device_mac}...")
        rules = get_rules(device_mac)
        print(f"{len(rules)} rules loaded")
        
        
        def process_packet(packet):
            if is_allowed(packet, rules):
                print(f"ALLOWED: {packet.summary()}")
            else:
                print(f"BLOCKED: {packet.summary()}")
        sniff(filter=f"ether host {device_mac}", prn=process_packet)            
        
        
if __name__== "__main__":
    add_rule("16:2d:4d:de:e7:67", "142.250.80.46", 443, "TCP")
    print("Test rule added successfully")
    
    rules = get_rules("16:2d:4d:de:e7:67")
    print(f"Rules found: {len(rules)}")
    for rule in rules:
        print(f" Allowed: {rule[0]}:{rule[1]} ({rule[2]})")        