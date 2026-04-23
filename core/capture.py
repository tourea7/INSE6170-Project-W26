from scapy.all import sniff, wrpcap
import os
import datetime

stop_capture = False
pause_capture = False
#la fonction qui démarre la capture de paquets, prend en paramètre l'adresse MAC, le nom du fichier de sortie, le nombre de paquets à capturer et la durée de la capture
def start_capture(mac, filename, count=100, duration=None): 
    global stop_capture, pause_capture
    stop_capture = False
    pause_capture = False
    
    pcap_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'pcap')
    os.makedirs(pcap_folder, exist_ok=True)
    filepath = os.path.join(pcap_folder, filename)
    
    packets = []
    
    def packet_handler(packet): #la fonction qui traite chaque paquet capturé
        if stop_capture:
            return
        if not pause_capture:
            packets.append(packet)
        if count and len(packets) >= count:
            return
    
    if duration:
        sniff(filter=f"ether host {mac}", prn=packet_handler, timeout=duration, stop_filter=lambda x: stop_capture)
    else:
        sniff(filter=f"ether host {mac}", prn=packet_handler, count=count, stop_filter=lambda x: stop_capture)
    
    if packets:
        wrpcap(filepath, packets)
    
    return filepath
    

def stop():
    global stop_capture
    stop_capture = True

def pause():
    global pause_capture
    pause_capture = True

def resume():
    global pause_capture
    pause_capture = False
    
if __name__ == "__main__": #test le code en exécutant ce fichier directement
    print("Starting capture...")
    filepath = start_capture("16:2d:4d:de:e7:64", "test_capture.pcap", count=10)
    print(f"Capture saved: {filepath}")