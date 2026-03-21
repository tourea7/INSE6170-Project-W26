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
        msg['Subject'] = f"IPS Alert - Abnormal traffic detected on {device_ip}"
        msg['From'] = alert_email
        msg["To"] = alert_email
        
        server = smtplib.SMTP('smtp.gmail.com' , 587)
        server.starttls()
        server.login(alert_email, "APP_PASSWORDS")
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
          
          
          
def monitor_device(device_ip, device_mac, max_rate, n_minutes=5):
    print(f"Monitoring {device_ip} (max: {max_rate} KB/s) ...")
    
    while monitoring:
        current_rate = get_bandwitdh(device_ip)
        print(f"{device_ip}: {current_rate:.2f} KB/s")
        
        if current_rate > max_rate:
            print(f"Alert : Abnormal traffic on {device_ip}")
            log_traffic(device_mac)
            send_alert(device_ip, current_rate)
            
            time.sleep(1)
            
def start_monitoring(device_ip, device_mac, max_rate, n_minutes=5):
    global monitoring
    monitoring = True
    
    thread = threading.Thread(target=monitor_device, args=(device_ip, device_mac, max_rate, n_minutes))
    thread.daemon = True
    thread.start()
    print(f"Monitoring started for {device_ip}")

def stop_monitoring():
    global monitoring
    monitoring = False
    print("Monitoring stopped") 
    
if __name__ == "__main__":
    start_monitoring("172.20.10.1", "16:2d:4d:de:e7:64", max_rate=100)
    
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        pass
    
    stop_monitoring()
    print("Test finished")               