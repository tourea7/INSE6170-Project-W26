from scapy.all import sniff, wrpcap
import os
import datetime

stop_capture = False

def start_capture(mac, filename, count=100):
    #Create pcap file
    pcap_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'pcap')
    os.makedirs(pcap_folder, exist_ok=True)
    #Roadmap for capture
    filepath = os.path.join(pcap_folder, filename)
    
    #Capture packets
    packets = sniff(filter=f"ether host {mac}", count=count)
    wrpcap(filepath, packets)
    
    #Return roadmap
    return filepath
    
#Stop capture
def stop():
    global stop_capture
    stop_capture = True
    
if __name__ == "__main__":
    print("Starting capture...")
    filepath = start_capture("16:2d:4d:de:e7:64", "test_capture.pcap", count=10)
    print(f"Capture saved: {filepath}")