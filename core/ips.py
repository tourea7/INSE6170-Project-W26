import psutil
import time
import smtplib
import threading
from email.mime.text import MIMEText
from scapy.all import sniff, wrpcap
import os

monitoring = False
alert_email = "angelkssi1@gmail.com"

def get_bandwitdh (device_ip):
    

    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()
    
    
    # Calculates bytes sent and received 
    bytes_sent = net2.bytes_sent - net1.bytes_sent
    bytes_recv = net2.bytes_recv - net1.bytes_recv
    
    total_kbps = (bytes_sent + bytes_recv) / 1024
    return total_kbps

def send_alert(device_ip, current_rate):
    try:
        msg = MIMEText(f"Alert: Device {device_ip} is behaving abnormal. Current data rate : {current_rate:.2f} KB/s")
        msg['Sunject'] = f"IPS Alert - Abnormal traffic detected on {device_ip}"
        msg['From'] = alert_email
        msg["To"] = alert_email
        
        server = smtplib.SMTP('smtp.gmail.com' , 587)
        server.starttls()
        server.login(alert_email, "KTy@2022")
        server.send_message(msg)
        server.quit()
        print(f"Alert email sent for {device_ip}")
        
    except Exception as e:
        print(f"Email error: {e}")
        
def log_traffic(device_mac):
    print(f"Logging traffic for {device_mac} for 10 seconds...")
    pcap_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'pcap')
    os.makedirs(pcap_folder, exist_ok=True)
    
    filename = f"alert_{device_mac.replace(':', '-')}_{int(time.time())}.pcap"
    filepath = os.path.join(pcap_folder, filename)
    
    packets = sniff(filter=f"ether host {device_mac}", timeout=10)
    wrpcap(filepath, packets)
    print(f"Traffic logged: {filepath}")
    return filepath        
          