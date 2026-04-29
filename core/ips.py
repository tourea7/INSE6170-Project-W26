import psutil
import time
import smtplib
import threading
from email.mime.text import MIMEText
from scapy.all import sniff, wrpcap
import sqlite3
import os
import subprocess 

monitoring = False
alert_email = "your_email@gmail.com"  # Replace with your Gmail address for receiving alerts

def get_min_rate(device_mac): 
    """Get minimum data rate for a device from database"""
    try:
        DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db')
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT min_rate FROM devices WHERE mac = ?", (device_mac,))
        result = cursor.fetchone()
        conn.close()
        if result and result[0]:
            return result[0]
        return 10
    except:
        return 10

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
        server.login(alert_email, "your_app_password") # Replace with your Gmail app passwords
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
        
def throttle_device(device_ip, min_rate, n_minutes): 
    print(f"Throttling {device_ip} to {min_rate} KB/s for {n_minutes} minutes...")
    try:
        subprocess.run([
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name=throttle_{device_ip}",
            "protocol=TCP",
            "dir=in",
            f"remoteip={device_ip}",
            "action=block"
        ], capture_output=True)
        
        print(f"Device {device_ip} throttled for {n_minutes} minutes")
    
        time.sleep(n_minutes * 60)
        
        subprocess.run([
            "netsh", "advfirewall", "firewall", "delete", "rule",
            f"name=throttle_{device_ip}"
        ], capture_output=True)
        
        print(f"Throttle removed for {device_ip}")
        
    except Exception as e:
        print(f"Throttle error: {e}")          
          
       
def monitor_device(device_ip, device_mac, max_rate, n_minutes=5): 
    print(f"Monitoring {device_ip} (max: {max_rate} KB/s) ...")
    
    while monitoring:
        current_rate = get_bandwitdh(device_ip)
        # Save to database
        conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db'))
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bandwidth_history (device_mac, timestamp, data_rate)
            VALUES (?, datetime('now'), ?)
        """, (device_mac, current_rate))
        conn.commit()
        conn.close()
        print(f"{device_ip}: {current_rate:.2f} KB/s")
        
        if current_rate > max_rate:
            print(f"Alert : Abnormal traffic on {device_ip}")
            # Save alert to database
            alert_conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', 'data', 'devices.db'))
            alert_cursor = alert_conn.cursor()
            alert_cursor.execute("""
                INSERT INTO alerts (device_ip, device_mac, timestamp, data_rate)
                VALUES (?, ?, datetime('now'), ?)
            """, (device_ip, device_mac, current_rate))
            alert_conn.commit()
            alert_conn.close()
            log_traffic(device_mac)
            send_alert(device_ip, current_rate)
            
            min_rate = get_min_rate(device_mac)
            throttle_thread = threading.Thread(
                target=throttle_device,
                args=(device_ip, min_rate, n_minutes)
            )
            throttle_thread.daemon = True
            throttle_thread.start()
            
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