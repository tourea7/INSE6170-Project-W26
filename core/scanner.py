from scapy.all import ARP , Ether , srp
import datetime
import requests

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
    
if __name__ == "__main__":
    devices = scan_networks()
    print(f"\n{len(devices)} devices found:")
    for d in devices:
        print(f"IP: {d['ip']} MAC: {d['mac']} Vendor: {d['vendor']}")
        