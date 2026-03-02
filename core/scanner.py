from scapy.all import ARP , Ether , srp
import datetime

def scan_networks(network="172.30.0.0/20"):
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
            "last_seen": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        }
        devices.append(device)
        
    return devices

if __name__ == "__main__":
    devices = scan_networks()
    print(f"\n{len(devices)} devices found:")
    for d in devices:
        print(f"IP: {d['ip']} MAC: {d['mac']}")
        